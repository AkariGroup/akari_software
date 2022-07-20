package util

import "os"

func PathExists(p string) bool {
	_, err := os.Stat(p)
	return err == nil
}

func DirExists(p string) bool {
	stat, err := os.Stat(p)
	return err == nil && stat.IsDir()
}

func FileExists(p string) bool {
	stat, err := os.Stat(p)
	return err == nil && !stat.IsDir()
}
