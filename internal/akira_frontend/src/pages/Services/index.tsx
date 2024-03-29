import useAspidaSWR from "@aspida/swr";
import { Box, Button, Container, Stack, Typography } from "@mui/material";
import { useCallback, useState } from "react";
import {
  Akira_protoCreateServiceRequest,
  Akira_protoService,
} from "../../api/@types";
import { ServiceList } from "../../components/ServiceList";
import { ServiceEditDrawer } from "./edit";
import { useApiClient } from "../../hooks/api";
import { ServiceCreateDrawer } from "./create";
import AddIcon from "@mui/icons-material/Add";
import { SubmitHandler } from "react-hook-form";
import { useSetBackdropValue } from "../../contexts/BackdropContext";

export function Services() {
  const client = useApiClient();
  const { data, error, mutate } = useAspidaSWR(client?.services, {
    enabled: !!client,
    refreshInterval: 5 * 1000, // in ms
  });
  const [createDrawerOpened, setCreateDrawerOpened] = useState(false);
  const [targetEditService, setTargetEditService] =
    useState<Akira_protoService | null>(null);
  const setBusy = useSetBackdropValue();

  const onServiceCreate: SubmitHandler<Akira_protoCreateServiceRequest> =
    useCallback(
      async (data) => {
        if (!client) return;

        setBusy(true);
        try {
          await client.services.post({
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
    async (target: Akira_protoService) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.services._id(target.id).start.post();
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, mutate, setBusy]
  );

  const onStopService = useCallback(
    async (target: Akira_protoService, terminate: boolean) => {
      if (!client || !target.id) return;
      setBusy(true);
      try {
        await client.services._id(target.id).stop.post({
          body: { terminate: terminate },
        });
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, mutate]
  );

  const onTerminate = useCallback(
    async (target: Akira_protoService) => {
      if (!client || !target.id) return;
      setBusy(true);
      try {
        await client.services._id(target.id).terminate.post();
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, mutate]
  );

  const onLaunchService = useCallback(
    async (target: Akira_protoService) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        const res = await client.services._id(target.id).open.get({
          query: {
            apiHostname: window.location.hostname,
          },
        });
        const url = res.body.url;
        window.open(url, "_blank", "noopener,noreferrer");
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy]
  );

  const onRemoveService = useCallback(
    async (target: Akira_protoService) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.services._id(target.id).remove.post();
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, mutate]
  );

  const onAutoStartService = useCallback(
    async (target: Akira_protoService) => {
      if (!client || !target.id) return;

      setBusy(true);
      try {
        await client.services._id(target.id).auto_start.post({
          body: { autoStart: !target.autoStart },
        });
        mutate?.();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, mutate]
  );

  if (!data?.services || error) {
    return <></>;
  }

  return (
    <Container maxWidth="xl">
      <Stack margin={1} spacing={1}>
        {createDrawerOpened ? (
          <ServiceCreateDrawer
            client={client}
            onClose={() => {
              setCreateDrawerOpened(false);
            }}
            onSubmit={onServiceCreate}
          />
        ) : (
          <></>
        )}
        {targetEditService && (
          <ServiceEditDrawer
            service={targetEditService}
            client={client}
            onClose={() => {
              mutate();
              setTargetEditService(null);
            }}
          />
        )}
        <Typography variant="h4" mb={1}>
          サービス
        </Typography>
        <Box pb={2}>
          <Typography variant="h5" mb={1}>
            ユーザーサービス一覧
          </Typography>
          <Box mb={1}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              color="success"
              onClick={() => setCreateDrawerOpened(true)}
            >
              新規作成
            </Button>
          </Box>
          <ServiceList
            services={data.services.filter((x) => x.type === "USER")}
            onStart={onStartService}
            onStop={onStopService}
            onTerminate={onTerminate}
            onLaunch={onLaunchService}
            onRemove={onRemoveService}
            onEdit={setTargetEditService}
            onAutoStart={onAutoStartService}
          />
        </Box>
        <Box>
          <Typography variant="h5" mb={1}>
            システムサービス一覧
          </Typography>
          <ServiceList
            services={data.services.filter((x) => x.type === "SYSTEM")}
            onStart={onStartService}
            onStop={onStopService}
            onTerminate={onTerminate}
            onAutoStart={onAutoStartService}
          />
        </Box>
      </Stack>
    </Container>
  );
}
