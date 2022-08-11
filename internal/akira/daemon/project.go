package daemon

import (
	"context"
	"fmt"

	"github.com/go-playground/validator/v10"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"

	"github.com/AkariGroup/akari_software/internal/akira/project"
	"github.com/AkariGroup/akari_software/internal/akira/proto"
)

type ProjectServicer struct {
	da *Daemon

	proto.UnimplementedProjectServiceServer
}

func NewProjectServicer(d *Daemon) (*ProjectServicer, error) {
	return &ProjectServicer{
		da: d,
	}, nil
}

func projectManifestToPb(p project.ProjectManifest) *proto.ProjectManifest {
	return &proto.ProjectManifest{
		Name:        p.Name,
		Description: p.Description,
		Author:      p.Author,
		Url:         p.Url,
		GitUrl:      p.GitUrl,
	}
}

func projectToPb(p project.Project) *proto.Project {
	return &proto.Project{
		Id:       p.Id(),
		Manifest: projectManifestToPb(p.Manifest()),
		Path:     p.Path(),
	}
}

func pbToProjectManifest(pb *proto.ProjectManifest) project.ProjectManifest {
	return project.ProjectManifest{
		Name:        pb.Name,
		Description: pb.Description,
		Author:      pb.Author,
		Url:         pb.Url,
		GitUrl:      pb.GitUrl,
	}
}

func (s *ProjectServicer) CreateLocalProject(ctx context.Context, r *proto.CreateLocalProjectRequest) (*proto.Project, error) {
	m := pbToProjectManifest(r.Manifest)
	v := validator.New()
	if err := v.Struct(m); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("invalid manifest: %#v", err))
	}

	t, ok := s.da.templates.LookupTemplate(r.TemplateId)
	if !ok {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("template doesn't exist: %#v", r.TemplateId))
	}

	if p, err := s.da.projects.CreateProject(r.Dirname, m, t); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error while creating a project: %#v", err))
	} else {
		return projectToPb(p), nil
	}
}

func (s *ProjectServicer) EditProject(ctx context.Context, r *proto.EditProjectRequest) (*proto.Project, error) {
	// TODO: Implement
	return nil, status.Errorf(codes.Unimplemented, "method EditProject not implemented")
}

func (s *ProjectServicer) GetProject(ctx context.Context, r *proto.GetProjectRequest) (*proto.Project, error) {
	p, ok := s.da.projects.GetProject(r.Id)
	if !ok {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("project doesn't exist: %#v", r.Id))
	}

	return projectToPb(p), nil
}

func (s *ProjectServicer) ListProjects(ctx context.Context, r *emptypb.Empty) (*proto.ListProjectsResponse, error) {
	ps := s.da.projects.ListProjects()
	var protos []*proto.Project
	for _, p := range ps {
		protos = append(protos, projectToPb(p))
	}

	return &proto.ListProjectsResponse{
		Projects: protos,
	}, nil
}

func templateToPb(t project.Template) *proto.Template {
	meta := t.Metadata()
	return &proto.Template{
		Id:          t.Id(),
		Name:        meta.Name,
		Version:     meta.Version,
		Description: meta.Description,
		Author:      meta.Author,
		Url:         meta.Url,
		Tags:        meta.Tags,
	}
}

func (s *ProjectServicer) ListTemplates(ctx context.Context, r *emptypb.Empty) (*proto.ListTemplatesResponse, error) {
	ts := s.da.templates.ListTemplates()
	var protos []*proto.Template
	for _, t := range ts {
		protos = append(protos, templateToPb(t))
	}

	return &proto.ListTemplatesResponse{
		Templates: protos,
	}, nil
}
