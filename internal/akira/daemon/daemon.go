package daemon

import ()

type Daemon struct {
}

func NewDaemon() (*Daemon, error) {
	return &Daemon{}, nil
}
