import useAspidaSWR from "@aspida/swr";
import { Box, Button, Container, Stack, Typography } from "@mui/material";
import { useCallback, useState } from "react";
import {
  Akira_protoCreateInstanceRequest,
  Akira_protoServiceInstance,
} from "../../api/@types";
import { InstanceList } from "../../components/InstanceList";
import { useApiClient } from "../../hooks/api";
import { InstanceCreateDrawer } from "./create";
import AddIcon from "@mui/icons-material/Add";
import { SubmitHandler } from "react-hook-form";
import { useSetBackdropValue } from "../../contexts/BackdropContext";

export function Services() {
  const client = useApiClient();
  const { data, error, mutate } = useAspidaSWR(client?.instances, {
    enabled: !!client,
    refreshInterval: 5 * 1000, // in ms
  });
  const [createDrawerOpened, setCreateDrawerOpened] = useState(false);
  const setBusy = useSetBackdropValue();

  const onInstanceCreate: SubmitHandler<Akira_protoCreateInstanceRequest> =
    useCallback(
      async (data) => {
        if (!client) return;

        // TODO: Handle error (e.g. Directory name conflicts)
        setBusy(true);
        try {
          await client.instances.post({
            body: data,
          });
          setCreateDrawerOpened(false);
          mutate();
        } finally {
          setBusy(false);
        }
      },
      [client, setBusy, setCreateDrawerOpened, mutate]
    );

  const onStartService = useCallback(
    async (target: Akira_protoServiceInstance) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.instances._id(target.id).start.post();
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, mutate, setBusy]
  );

  const onStopService = useCallback(
    async (target: Akira_protoServiceInstance, terminate: boolean) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.instances._id(target.id).stop.post({
          body: { terminate: terminate },
        });
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, mutate]
  );

  const onLaunchService = useCallback(
    async (target: Akira_protoServiceInstance) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        const res = await client.instances._id(target.id).open.get();
        const url = res.body.url;
        window.open(url, "_blank", "noopener,noreferrer");
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy]
  );

  const onRemoveService = useCallback(
    async (target: Akira_protoServiceInstance) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.instances._id(target.id).remove.post();
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, mutate]
  );

  if (!data?.instances || error) {
    return <></>;
  }

  return (
    <Container maxWidth="xl">
      <Stack margin={1} spacing={1}>
        {createDrawerOpened ? (
          <InstanceCreateDrawer
            client={client}
            onClose={() => {
              setCreateDrawerOpened(false);
            }}
            onSubmit={onInstanceCreate}
          />
        ) : (
          <></>
        )}

        <Typography variant="h4" mb={1}>
          インスタンス一覧
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            color="success"
            onClick={() => setCreateDrawerOpened(true)}
          >
            新規作成
          </Button>
        </Box>
        <InstanceList
          instances={data.instances}
          onStart={onStartService}
          onStop={onStopService}
          onLaunch={onLaunchService}
          onRemove={onRemoveService}
        />
      </Stack>
    </Container>
  );
}
