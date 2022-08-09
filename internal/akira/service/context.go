package service

import "context"

type ctxAsync struct{}

func SetAsync(parent context.Context, async bool) context.Context {
	return context.WithValue(parent, ctxAsync{}, async)
}

func GetAsync(ctx context.Context) bool {
	if v, ok := ctx.Value(ctxAsync{}).(bool); ok {
		return v
	} else {
		return false
	}
}
