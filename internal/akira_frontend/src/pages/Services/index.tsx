import useAspidaSWR from "@aspida/swr";
import { Box, Container, Stack, Typography } from "@mui/material";
import { useCallback } from "react";
import { Akira_protoServiceInstance } from "../../api/@types";
import { InstanceList } from "../../components/InstanceList";
import { useApiClient } from "../../hooks/api";

export function Services() {
  const client = useApiClient();
  const { data, error } = useAspidaSWR(client?.instances, {
    enabled: !!client,
  });

  const onStartService = useCallback(
    async (target: Akira_protoServiceInstance) => {
      if (!client || !target.id) return;

      // TODO: Show waiting icon
      await client.instances._id(target.id).start.post();
    },
    [client]
  );

  const onStopService = useCallback(
    async (target: Akira_protoServiceInstance, terminate: boolean) => {
      if (!client || !target.id) return;

      // TODO: Show waiting icon
      await client.instances._id(target.id).stop.post({
        body: { terminate: terminate },
      });
    },
    [client]
  );

  const onLaunchService = useCallback(
    async (target: Akira_protoServiceInstance) => {
      if (!client || !target.id) return;

      const res = await client.instances._id(target.id).open.get();
      const url = res.body.url;
      console.log(url);
    },
    [client]
  );

  const onRemoveService = useCallback(
    async (target: Akira_protoServiceInstance) => {
      if (!client || !target.id) return;

      // TODO: Show waiting icon
      await client.instances._id(target.id).remove.post();
    },
    [client]
  );

  if (!data?.instances || error) {
    return <></>;
  }

  return (
    <Container maxWidth="xl">
      <Stack margin={1}>
        <Box>
          <Typography variant="h4" mb={1}>
            Instances
          </Typography>
          <InstanceList
            instances={data.instances}
            onStart={onStartService}
            onStop={onStopService}
            onLaunch={onLaunchService}
            onRemove={onRemoveService}
          />
        </Box>
      </Stack>
    </Container>
  );
}
