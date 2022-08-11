import { Box, Container, Paper, Tab, Tabs } from "@mui/material";
import { ReactNode, useState } from "react";
import { CreateProjectFromTemplate } from "./createFromTemplate";
import { CreateProjectFromGit } from "./createFromGit";

type TabPanelProps = {
  visible: boolean;
  children?: ReactNode;
};

function TabPanel({ visible, children }: TabPanelProps) {
  if (!visible) {
    return <></>;
  }
  return <Box mt={1}>{children}</Box>;
}

export function ProjectsCreate() {
  const [mode, setMode] = useState(0);
  return (
    <Container maxWidth="xl">
      <Paper sx={{ mt: 2, pb: 1 }}>
        <Tabs value={mode}>
          <Tab label="テンプレートから作成" value={0} onClick={() => {
            setMode(0);
          }} />
          <Tab label="Gitレポジトリから作成" value={1} onClick={() => {
            setMode(1);
          }} />
        </Tabs>
        <TabPanel visible={mode === 0}>
          <CreateProjectFromTemplate />
        </TabPanel>
        <TabPanel visible={mode === 1}>
          <CreateProjectFromGit />
        </TabPanel>
      </Paper>
    </Container>
  );
}
