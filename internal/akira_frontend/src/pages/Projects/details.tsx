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
import { Navigate, useSearchParams } from "react-router-dom";
import { OpenProjectWithServiceButton } from "../../components/OpenProjectWithServiceButton";
import { useApiClient } from "../../hooks/api";

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
                <Typography mt={1} variant="body2">
                  {project.manifest?.author}
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
              <OpenProjectWithServiceButton />
            </Box>
            <Box>
              <Typography variant="subtitle2">Project info</Typography>
              <Divider />
              <Typography mt={1} variant="body2" color="textSecondary">
                URL: {project.manifest?.url}
              </Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2">Metadata</Typography>
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
