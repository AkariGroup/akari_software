import useAspidaSWR from "@aspida/swr";
import { GridView, } from "@mui/icons-material";
import {
  Stack, Container, Paper, Tab, Tabs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  Button,
} from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import { ReactNode, useState, } from "react";
import { LayoutRouteProps, Link } from "react-router-dom";
import { NewProjectButtonCard, ProjectCard } from "../../components/ProjectCard";
import { ProjectList } from "../../components/ProjectList";
import { useApiClient } from "../../hooks/api";

/*function LayoutView(props: LayoutRouteProps) {
  const layout = props;
  return (
    layout === 'gridView' ? <GridView /> : <ListView />
  )
}

function SwitchBetweenLayout() {
  const [layout, setLayout] = useState('listView');

  const onClickButton = (layoutInfo: string) => {
    const currentLayout = layoutInfo; // gets 'listView or gridView
    setLayout(currentLayout); // only set if state is changed.
  }

  return (
    //HTML for 2 buttons with click handler
    <LayoutView layout={layout} />

  )
}*/

function Header() {
  return (
    <TableHead>
      <TableRow>
        <TableCell sx={{ width: 300 }}>プロジェクト名</TableCell>
        <TableCell sx={{ width: 300 }}>作者名</TableCell>
        <TableCell sx={{ width: 600 }}>概要</TableCell>
        <TableCell ></TableCell>
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

  const onClickButton = (layoutInfo: number) => {
    const currentLayout = layoutInfo; // gets 'listView or gridView
    //setLayout(currentLayout); // only set if state is changed.
  }


  return (
    <Container maxWidth="xl">
        <Stack spacing={2} sx={{ margin: 1 }} direction="row" >
          <Tabs value={mode}>
            <Tab label="Card" value={0} onClick={() => {
              setMode(0);
            }} />
            <Tab label="Table" value={1} onClick={() => {
              setMode(1);
            }} />
          </Tabs>
      </Stack>
      <Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          color="success"
          component={Link} to="/projects/create"
        >
          新規プロジェクト
        </Button>
      </Box>
      <Header />
        {data.projects?.map((p) => (
          <ProjectList key={p.id} project={p} />
        ))}
    </Container>

    /*<Stack spacing={2} sx={{ margin: 1 }} direction="row">
        <NewProjectButtonCard />
      {data.projects?.map((p) => (
        <ProjectCard key={p.id} project={p} />
      ))}
    </Stack>*/
  );
}
