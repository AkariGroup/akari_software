import useAspidaSWR from "@aspida/swr";
import {
  Stack,
  Container,
  TableCell,
  TableHead,
  TableRow,
  Button,
  Grid,
  Table,
} from "@mui/material";
import GridViewIcon from "@mui/icons-material/GridView";
import TableRowsIcon from "@mui/icons-material/TableRows";
import AddIcon from "@mui/icons-material/Add";
import { useState } from "react";
import { Link } from "react-router-dom";
import {
  NewProjectButtonCard,
  ProjectCard,
} from "../../components/ProjectCard";
import { ProjectListItem, ProjectListHeader } from "./ProjectList";
import { useApiClient } from "../../hooks/api";

const projectDispModeKey = "projectDispMode"
export function Projects() {
  const [mode, setMode] = useState(
    localStorage.getItem(projectDispModeKey) === "1" ? 1 : 0
  );
  const client = useApiClient();

  const { data, error } = useAspidaSWR(client?.projects, { enabled: !!client });
  let element = null;
  if (!mode) {
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
      <div style={{ display: mode ? "" : "none" }}>
        <Stack spacing={2} sx={{ margin: 1 }} direction="row">
          <NewProjectButtonCard />
          {data?.projects?.map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </Stack>
      </div>
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
            variant={mode ? "contained" : undefined}
            onClick={() => {
              localStorage.setItem(projectDispModeKey, "1");
              setMode(1);
            }}
          >
            <GridViewIcon />
          </Button>
          <Button
            variant={mode ? undefined : "contained"}
            onClick={() => {
              localStorage.setItem(projectDispModeKey, "0");
              setMode(0);
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
