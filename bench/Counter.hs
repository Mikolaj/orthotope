-- Copyright 2020 Google LLC
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

-- The count of the instructions the calling thread executes in user space,
-- by Linux's perf_event_open, as perf stat -e instructions:u counts them,
-- and the pinning of the process to one CPU, by sched_setaffinity, both
-- through the C library's syscall: off Linux neither is there, and each says
-- so.
{-# LANGUAGE CApiFFI, CPP #-}
module Counter (Counter, open, counted, pin) where

#if defined(linux_HOST_OS)
import Control.Exception (IOException, try)
import Control.Monad (forM)
import Data.Bits (shiftL, (.|.))
import Data.Char (isDigit)
import Data.Word (Word32, Word8)
import Foreign.C.Error (errnoToIOError, getErrno)
import Foreign.C.Types (CInt (..), CLong (..), CSize (..), CULong (..))
import Foreign.Marshal.Alloc (alloca, allocaBytes)
import Foreign.Marshal.Utils (fillBytes)
import Foreign.Ptr (Ptr)
import Foreign.Storable (peek, pokeByteOff)
import System.Directory (listDirectory)
import System.Posix.Types (CSsize (..))
#else
import Foreign.C.Types (CInt)
#endif
import Data.Word (Word64)

-- | An open counter of the calling thread's instructions in user space.
newtype Counter = Counter CInt

-- | The instructions the counter's thread executes in user space running the
-- action.
counted :: Counter -> IO () -> IO Word64

-- | A counter of the calling thread's instructions, or why there is none.
open :: IO (Either String Counter)

-- | Every thread of the process pinned to the CPU, or why it is not.
pin :: Int -> IO (Either String ())

#if defined(linux_HOST_OS)
foreign import capi "sys/syscall.h value SYS_perf_event_open"
  sysPerfEventOpen :: CLong
foreign import capi "sys/syscall.h value SYS_sched_setaffinity"
  sysSchedSetaffinity :: CLong
foreign import capi "linux/perf_event.h value PERF_TYPE_HARDWARE"
  typeHardware :: Word32
foreign import capi "linux/perf_event.h value PERF_COUNT_HW_INSTRUCTIONS"
  hwInstructions :: Word64
foreign import capi "linux/perf_event.h value PERF_ATTR_SIZE_VER0"
  attrSizeVer0 :: Word32
foreign import capi "linux/perf_event.h value PERF_EVENT_IOC_RESET"
  iocReset :: CULong
foreign import capi "linux/perf_event.h value PERF_EVENT_IOC_ENABLE"
  iocEnable :: CULong
foreign import capi "linux/perf_event.h value PERF_EVENT_IOC_DISABLE"
  iocDisable :: CULong
-- syscall (SYS_perf_event_open, attr, pid, cpu, group_fd, flags)
foreign import capi unsafe "unistd.h syscall"
  perfEventOpen :: CLong -> Ptr () -> CInt -> CInt -> CInt -> CULong
                -> IO CLong
-- syscall (SYS_sched_setaffinity, tid, the mask's size, the mask)
foreign import capi unsafe "unistd.h syscall"
  schedSetaffinity :: CLong -> CInt -> CSize -> Ptr Word8 -> IO CLong
foreign import capi unsafe "sys/ioctl.h ioctl"
  ioctl :: CInt -> CULong -> CInt -> IO CInt
foreign import capi unsafe "unistd.h read"
  readFd :: CInt -> Ptr Word64 -> CSize -> IO CSsize

-- The failure of the call named, by its errno.
failure :: String -> IO String
failure what = do
  e <- getErrno
  return $! show (errnoToIOError what e Nothing Nothing)

-- The attributes, the first PERF_ATTR_SIZE_VER0 bytes of a struct
-- perf_event_attr, are its type, its size, its config and, at byte 40, its
-- flags: disabled (bit 0), exclude_kernel (bit 5) and exclude_hv (bit 6),
-- those of perf's :u.  The counter is the thread's (pid 0) on any CPU (-1).
open = allocaBytes (fromIntegral attrSizeVer0) $ \ p -> do
  fillBytes p 0 (fromIntegral attrSizeVer0)
  pokeByteOff p 0 typeHardware
  pokeByteOff p 4 attrSizeVer0
  pokeByteOff p 8 hwInstructions
  pokeByteOff p 40 (1 .|. shiftL 1 5 .|. shiftL 1 6 :: Word64)
  fd <- perfEventOpen sysPerfEventOpen p 0 (-1) (-1) 0
  if fd < 0
    then Left <$> failure "perf_event_open"
    else return $ Right $ Counter $ fromIntegral fd

counted (Counter fd) act = do
  _ <- ioctl fd iocReset 0
  _ <- ioctl fd iocEnable 0
  act
  _ <- ioctl fd iocDisable 0
  alloca $ \ b -> do
    r <- readFd fd b 8
    if r == 8 then peek b else ioError (userError "read of the counter")

-- Each thread of /proc/self/task, the RTS's ticker among them, is pinned; a
-- thread started later inherits its starter's mask.
pin cpu
  | cpu < 0 || cpu >= 8 * maskBytes = return $ Left $ "no CPU " ++ show cpu
  | otherwise = allocaBytes maskBytes $ \ mask -> do
      fillBytes mask 0 maskBytes
      pokeByteOff mask (cpu `div` 8) (shiftL 1 (cpu `mod` 8) :: Word8)
      tasks <- try (listDirectory "/proc/self/task")
      case tasks :: Either IOException [FilePath] of
        Left e -> return $ Left $ "/proc/self/task: " ++ show e
        Right ts -> do
          rs <- forM (filter (all isDigit) ts) $ \ t -> do
            r <- schedSetaffinity sysSchedSetaffinity (read t)
                                  (fromIntegral maskBytes) mask
            if r < 0 then Just <$> failure ("sched_setaffinity of " ++ t)
            else return Nothing
          return $ case [ e | Just e <- rs ] of
            [] -> Right ()
            e : _ -> Left e
 where
  maskBytes = 128
#else
open = return $ Left "perf_event_open: not on Linux"

counted _ act = act >> return 0

pin _ = return $ Left "sched_setaffinity: not on Linux"
#endif
