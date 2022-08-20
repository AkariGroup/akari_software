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

const enum DISP_MODE {
  TABLE,
  CARD
}

const projectDispModeKey = "projectDispMode"
export function Projects() {
  const [mode, setMode] = useState(() => localStorage.getItem(projectDispModeKey) === "TABLE" ? DISP_MODE.TABLE : DISP_MODE.CARD
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
            variant={mode === DISP_MODE.CARD ? "contained" : undefined}
            onClick={() => {
              localStorage.setItem(projectDispModeKey, "CARD");
              setMode(DISP_MODE.CARD);
            }}
          >
            <GridViewIcon />
          </Button>
          <Button
            variant={mode === DISP_MODE.TABLE ? "contained" : undefined}
            onClick={() => {
              localStorage.setItem(projectDispModeKey, "TABLE");
              setMode(DISP_MODE.TABLE);
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
