import useAspidaSWR from "@aspida/swr";
import {
  Box,
  Card,
  CardContent,
  Container,
  Divider,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import { Navigate, useSearchParams } from "react-router-dom";
import { OpenProjectWithServiceButton } from "../../components/OpenProjectWithServiceButton";
import { useApiClient } from "../../hooks/api";
import { useCallback } from "react";
import { Akira_protoServiceInstance } from "../../api/@types";
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
  const { data: instances } = useAspidaSWR(client?.instances, {
    enabled: !!client,
  });
  const setBusy = useSetBackdropValue();

  const onOpenProject = useCallback(
    async (s: Akira_protoServiceInstance) => {
      if (!client || !s.id || !project?.id) return;

      setBusy(true);
      try {
        const res = await client.instances._serviceId(s.id).open_project.get({
          query: { projectId: project.id },
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
      <Grid container mt={2} spacing={3}>
        <Grid item sm={12} md={9}>
          <Card>
            <CardContent>
              <Box mb={1}>
                <Typography variant="h4">{project.manifest?.name}</Typography>
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
                instances={instances?.instances}
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
