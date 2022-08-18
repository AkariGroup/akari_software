import useAspidaSWR from "@aspida/swr";
import {
  Stack,
  Container,
  TableCell,
  TableHead,
  TableRow,
  Button,
  Grid,
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
import { ProjectList } from "../../components/ProjectList";
import { useApiClient } from "../../hooks/api";

function Header() {
  return (
    <TableHead>
      <TableRow>
        <TableCell sx={{ width: 300 }}>プロジェクト名</TableCell>
        <TableCell sx={{ width: 300 }}>作者名</TableCell>
        <TableCell sx={{ width: 600 }}>概要</TableCell>
        <TableCell></TableCell>
      </TableRow>
    </TableHead>
  );
}
export function Projects() {
  const [mode, setMode] = useState(0);
  const client = useApiClient();

  const { data, error } = useAspidaSWR(client?.projects, { enabled: !!client });

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
              setMode(1);
            }}
          >
            <GridViewIcon />
          </Button>
          <Button
            variant={mode ? undefined : "contained"}
            onClick={() => {
              setMode(0);
            }}
          >
            <TableRowsIcon />
          </Button>
        </Stack>
      </Grid>
      <div style={{ display: mode ? "none" : "" }}>
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
            <Header />
            {data.projects?.map((p) => (
              <ProjectList key={p.id} project={p} />
            ))}
          </Container>
        </Grid>
      </div>
      <div style={{ display: mode ? "" : "none" }}>
        <Stack spacing={2} sx={{ margin: 1 }} direction="row">
          <NewProjectButtonCard />
          {data.projects?.map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </Stack>
      </div>
    </Grid>
  );
}
