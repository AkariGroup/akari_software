import useAspidaSWR from "@aspida/swr";
import { Stack } from "@mui/material";
import { NewProjectButtonCard, ProjectCard } from "../../components/ProjectCard";
import { useApiClient } from "../../hooks/api";

export function Projects() {
  const client = useApiClient();
  const { data, error } = useAspidaSWR(client?.projects, { enabled: !!client });

  if (!data || error) {
    return <></>;
  }

  return (
    <Stack spacing={2} sx={{ margin: 1 }} direction="row">
        <NewProjectButtonCard />
      {data.projects?.map((p) => (
        <ProjectCard key={p.id} project={p} />
      ))}
    </Stack>
  );
}
