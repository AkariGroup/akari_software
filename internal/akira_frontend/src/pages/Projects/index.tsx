import useAspidaSWR from "@aspida/swr";
import {
  Stack,
  Container,
  Button,
  Grid,
} from "@mui/material";
import GridViewIcon from "@mui/icons-material/GridView";
import TableRowsIcon from "@mui/icons-material/TableRows";
import AddIcon from "@mui/icons-material/Add";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  NewProjectButtonCard,
  ProjectCard,
} from "../../components/ProjectCard";
import { ProjectListItem, ProjectListHeader } from "./ProjectList";
import { useApiClient } from "../../hooks/api";

type DisplayMode = "card" | "table";

const projectDisplayModeKey = "projectDisplayMode"
export function Projects() {
  const [mode, setMode] = useState<DisplayMode>(() => localStorage.getItem(projectDisplayModeKey) as DisplayMode);
  const client = useApiClient();
  useEffect(() => {
    localStorage.setItem(projectDisplayModeKey,mode);
  }, [mode]);
  const { data, error } = useAspidaSWR(client?.projects, { enabled: !!client });
  let element = null;
  if (mode==="table") {
    element = (
      <Grid container>
        <Container maxWidth="xl">
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            color="success"
            component={Link}
            to="/projects/create"
          >
            新規プロジェクト
          </Button>
          <ProjectListHeader />
          {data?.projects?.map((p) => (
            <ProjectListItem key={p.id} project={p} />
          ))}
        </Container>
      </Grid>
    );
  } else {
    element = (
      <Stack spacing={2} sx={{ margin: 1 }} direction="row">
        <NewProjectButtonCard />
        {data?.projects?.map((p) => (
          <ProjectCard key={p.id} project={p} />
        ))}
      </Stack>
    );
  }

  if (!data || error) {
    return <></>;
  }

  return (
    <Grid container>
      <Grid container justifyContent="flex-end">
        <Stack sx={{ margin: 1 }} direction="row">
          <Button
            variant={mode === "card" ? "contained" : undefined}
            onClick={() => {
              setMode("card");
            }}
          >
            <GridViewIcon />
          </Button>
          <Button
            variant={mode === "table" ? "contained" : undefined}
            onClick={() => {
              setMode("table");
            }}
          >
            <TableRowsIcon />
          </Button>
        </Stack>
      </Grid>
      {element}
    </Grid>
  );
}
