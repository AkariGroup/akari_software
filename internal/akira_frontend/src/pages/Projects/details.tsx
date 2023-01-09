import useAspidaSWR from "@aspida/swr";
import { NavLink } from "react-router-dom";
import {
  Box,
  Card,
  CardContent,
  Container,
  Divider,
  Grid,
  Stack,
  Typography,
  IconButton,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import PersonIcon from "@mui/icons-material/Person";
import EditIcon from "@mui/icons-material/Edit";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import { useNavigate, Navigate, useSearchParams } from "react-router-dom";
import { OpenProjectWithServiceButton } from "../../components/OpenProjectWithServiceButton";
import { useApiClient } from "../../hooks/api";
import { useCallback } from "react";
import { Akira_protoService } from "../../api/@types";
import { useSetBackdropValue } from "../../contexts/BackdropContext";

export function ProjectsDetails() {
  const [searchParams] = useSearchParams();
  const projectId = searchParams.get("id") as string;
  const client = useApiClient();
  const { data: project } = useAspidaSWR(client?.projects.detail, {
    query: {
      id: projectId,
    },
    enabled: !!projectId && !!client,
  });
  const { data: services } = useAspidaSWR(client?.services, {
    enabled: !!client,
  });
  const navigate = useNavigate();
  const editPage = () => {
    navigate(`/projects/edit?id=${projectId}`);
  };
  const setBusy = useSetBackdropValue();
  const onOpenProject = useCallback(
    async (s: Akira_protoService) => {
      if (!client || !s.id || !project?.id) return;

      setBusy(true);
      try {
        const res = await client.services._id(s.id).open_project.get({
          query: {
            apiHostname: window.location.hostname,
            projectId: project.id,
          },
        });
        const url = res.body.url;
        window.open(url, "_blank", "noopener,noreferrer");
      } finally {
        setBusy(false);
      }
    },
    [client, project, setBusy]
  );

  if (!projectId) {
    return <Navigate to="/projects" />;
  }

  if (!project) {
    return <></>;
  }

  return (
    <Container maxWidth="xl">
      <Grid margin={1}>
        <IconButton type="button" component={NavLink} to="/projects">
          <ArrowBackIcon />
        </IconButton>
      </Grid>
      <Grid container>
        <Grid item sm={12} md={9}>
          <Card>
            <CardContent>
              <Box mb={1}>
                <Box sx={{ display: "flex" }}>
                  <Typography variant="h4">{project.manifest?.name}</Typography>
                  &nbsp;
                  <Typography sx={{ flexGrow: 1 }}>
                    <IconButton aria-label="Edit" onClick={editPage}>
                      <EditIcon />
                    </IconButton>
                  </Typography>
                  <IconButton>
                    <MoreVertIcon />
                  </IconButton>
                </Box>
                <Typography
                  mt={1}
                  variant="body2"
                  display="flex"
                  alignItems="center"
                >
                  <PersonIcon />
                  &nbsp;{project.manifest?.author}
                </Typography>
              </Box>
              <Divider />
              <Box mt={1}>{project.manifest?.description}</Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item sm={12} md={3} sx={{ overflowWrap: "anywhere" }}>
          <Stack spacing={3}>
            <Box>
              <OpenProjectWithServiceButton
                services={services?.services}
                onSelected={onOpenProject}
              />
            </Box>
            <Box>
              <Typography variant="subtitle2">プロジェクト情報</Typography>
              <Divider />
              <Typography mt={1} variant="body2" color="textSecondary">
                URL: {project.manifest?.url}
              </Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2">メタデータ</Typography>
              <Divider />
              <Typography mt={1} variant="body2" color="textSecondary">
                ID: {project.id}
                <br />
                Path: {project.path}
              </Typography>
            </Box>
          </Stack>
        </Grid>
      </Grid>
    </Container>
  );
}
