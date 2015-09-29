import os


if __name__ == '__main__':
    for fname in os.listdir('.'):
        if fname.endswith('_stip.pkl'):
            # Get actual times
            st_atime = os.stat(fname).st_atime
            st_mtime = os.stat(fname).st_mtime
            st_ctime = os.stat(fname).st_ctime
            # Set utime
            dt = 13 * 3600
            atime = st_atime + dt
            mtime = st_mtime + dt
            os.utime(fname, (atime, mtime))
