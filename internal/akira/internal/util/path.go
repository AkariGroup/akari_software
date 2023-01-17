package util

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

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

func GetStem(p string) string {
	return strings.TrimSuffix(p, filepath.Ext(p))
}

var pathUnsafe = regexp.MustCompile("[^A-Za-z0-9-_]")

func SanitizeDirname(dirname string) string {
	return pathUnsafe.ReplaceAllLiteralString(dirname, "")
}
