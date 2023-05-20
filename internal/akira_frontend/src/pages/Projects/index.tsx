import useAspidaSWR from "@aspida/swr";
import { Stack, Container, Button, Grid } from "@mui/material";
import GridViewIcon from "@mui/icons-material/GridView";
import TableRowsIcon from "@mui/icons-material/TableRows";
import RefreshIcon from "@mui/icons-material/Refresh";
import AddIcon from "@mui/icons-material/Add";
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  NewProjectButtonCard,
  ProjectCard,
} from "../../components/ProjectCard";
import { ProjectListItem, ProjectListHeader } from "./ProjectList";
import { useApiClient } from "../../hooks/api";
import { Akira_protoProject } from "../../api/@types";
import { useSetBackdropValue } from "../../contexts/BackdropContext";

type DisplayMode = "card" | "table";

const projectDisplayModeKey = "projectDisplayMode";
export function Projects() {
  const [mode, setMode] = useState<DisplayMode>(
    () => localStorage.getItem(projectDisplayModeKey) as DisplayMode
  );

  const setBusy = useSetBackdropValue();
  const client = useApiClient();
  useEffect(() => {
    localStorage.setItem(projectDisplayModeKey, mode);
  }, [mode]);
  const { data, error, mutate } = useAspidaSWR(client?.projects, {
    enabled: !!client,
  });
  const refreshProjects = useCallback(async () => {
    if (!client) return;

    setBusy(true);
    try {
      await client.projects.refresh.post({
        body: {},
      });
      mutate();
    } finally {
      setBusy(false);
    }
  }, [client, mutate, setBusy]);

  const onRemove = useCallback(
    async (target: Akira_protoProject) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.projects.delete.post({ body: { id: target.id } });
        await client.projects.refresh.post({
          body: {},
        });
        mutate();
      } finally {
        setBusy(false);
      }
    },
    [client, mutate, setBusy]
  );

  const sortKey = useCallback(
    (lhs: Akira_protoProject, rhs: Akira_protoProject) => {
      const lhsState = lhs.manifest?.name ?? "";
      const rhsState = rhs.manifest?.name ?? "";
      return lhsState > rhsState ? 1 : -1;
    },
    []
  );
  let sortedProjects = data?.projects?.sort(sortKey);

  let element = null;
  if (mode === "table") {
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
          {sortedProjects?.map((p) => (
            <ProjectListItem key={p.id} project={p} onRemove={onRemove} />
          ))}
        </Container>
      </Grid>
    );
  } else {
    element = (
      <Grid container spacing={2} sx={{ margin: 1 }}>
        <Grid item xs="auto">
          <NewProjectButtonCard />
        </Grid>
        {sortedProjects?.map((p) => (
          <Grid item xs="auto">
            <ProjectCard key={p.id} project={p} onRemove={onRemove} />
          </Grid>
        ))}
      </Grid>
    );
  }

  if (!data || error) {
    return <></>;
  }

  return (
    <Grid container>
      <Grid xs display="flex" justifyContent="flex-end">
        <Button>
          <RefreshIcon fontSize="large" onClick={refreshProjects} />
        </Button>
        <Stack sx={{ margin: 2 }}></Stack>
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
