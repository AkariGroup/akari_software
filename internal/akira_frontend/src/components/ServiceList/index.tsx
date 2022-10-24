import useAspidaSWR from "@aspida/swr";
import {
  Box,
  Button,
  CircularProgress,
  Divider,
  Drawer,
  IconButton,
  Link,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import {
  Akira_protoServiceStatus,
  Akira_protoService,
  Akira_protoServiceImage,
} from "../../api/@types";
import {
  Controller,
  SubmitHandler,
  useForm,
} from "react-hook-form";
import LaunchIcon from "@mui/icons-material/Launch";
import PowerSettingsNewIcon from "@mui/icons-material/PowerSettingsNew";
import DeleteIcon from "@mui/icons-material/Delete";
import { useCallback, useState } from "react";
import { PowerDialog, PowerDialogResult } from "./powerDialog";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { RemoveDialog, RemoveDialogResult } from "./removeDialog";
import { ApiClient, useApiClient } from "../../hooks/api";
import { useSetBackdropValue } from "../../contexts/BackdropContext";
import { ValidationMessages } from "../../libs/messages";
import { useSearchParams } from "react-router-dom";

export interface EditServiceRequest {
  id: string;
  display_name: string;
  description: string;
}

export interface SetAutoStartRequest {
  id: string;
  auto_start: boolean;
}


type Props = {
  services: Akira_protoService[];
  onStart: (target: Akira_protoService) => void;
  onStop: (target: Akira_protoService, terminate: boolean) => void;
  onLaunch?: (target: Akira_protoService) => void;
  onRemove?: (target: Akira_protoService) => void;
};

function Header() {
  return (
    <TableHead>
      <TableRow>
        <TableCell>DisplayName</TableCell>
        <TableCell>Service</TableCell>
        <TableCell sx={{ width: 200 }}>Status</TableCell>
        <TableCell sx={{ width: 170 }}></TableCell>
      </TableRow>
    </TableHead>
  );
}

function Status({ status }: { status?: Akira_protoServiceStatus }) {
  let color = "primary";
  let bold = false;
  switch (status) {
    case "ERROR":
      color = "error.main";
      bold = true;
      break;
    case "RUNNING":
      color = "success.main";
      bold = true;
      break;
    case "STARTING":
      color = "info.main";
      break;
    case "STOPPED":
      color = "warning.main";
      bold = true;
      break;
    case "STOPPING":
      color = "warning.main";
      break;
    case "TERMINATED":
      color = "secondary.main";
      bold = true;
      break;
  }

  return (
    <Typography color={color} fontWeight={bold ? "bold" : undefined}>
      {status}
    </Typography>
  );
}

type PowerButtonProps = {
  service: Akira_protoService;
  onStart: (target: Akira_protoService) => void;
  onStop: (target: Akira_protoService, terminate: boolean) => void;
};

function PowerButton(props: PowerButtonProps) {
  const [powerDialogOpened, setPowerDialogOpened] = useState(false);
  const onPowerIconClicked = useCallback(() => {
    if (props.service.status === "RUNNING") {
      setPowerDialogOpened(true);
    } else {
      props.onStart(props.service);
    }
  }, [props, setPowerDialogOpened]);
  const onPowerConfirmation = useCallback(
    (d: PowerDialogResult) => {
      setPowerDialogOpened(false);
      if (d === PowerDialogResult.CANCEL) {
        return;
      } else {
        props.onStop(props.service, d === PowerDialogResult.TERMINATE);
      }
    },
    [props, setPowerDialogOpened]
  );
  const powerButtonDisabled =
    props.service.status === "STARTING" || props.service.status === "STOPPING";
  const powerIcon = (() => {
    if (powerButtonDisabled) {
      return <CircularProgress />;
    } else if (props.service.status === "RUNNING") {
      return <PowerSettingsNewIcon color="error" />;
    } else {
      return <PlayArrowIcon color="success" />;
    }
  })();

  return (
    <>
      {powerDialogOpened ? (
        <PowerDialog
          serviceName={props.service.displayName ?? ""}
          onResponse={onPowerConfirmation}
        />
      ) : null}
      <IconButton onClick={onPowerIconClicked} disabled={powerButtonDisabled}>
        {powerIcon}
      </IconButton>
    </>
  );
}

type RemoveButtonProps = {
  service: Akira_protoService;
  onRemove: (target: Akira_protoService) => void;
};

function RemoveButton(props: RemoveButtonProps) {
  const [opened, setOpened] = useState(false);
  const onConfirm = useCallback(
    (d: RemoveDialogResult) => {
      setOpened(false);
      if (d === RemoveDialogResult.CANCEL) {
        return;
      } else {
        props.onRemove(props.service);
      }
    },
    [props, setOpened]
  );
  return (
    <>
      {opened ? (
        <RemoveDialog
          serviceName={props.service.displayName ?? ""}
          onResponse={onConfirm}
        />
      ) : null}
      <IconButton onClick={() => setOpened(true)}>
        <DeleteIcon />
      </IconButton>
    </>
  );
}

type ServiceRowProps = {
  service: Akira_protoService;
  onStart: (target: Akira_protoService) => void;
  onStop: (target: Akira_protoService, terminate: boolean) => void;
  onLaunch?: (target: Akira_protoService) => void;
  onRemove?: (target: Akira_protoService) => void;
};

function ServiceImageLink({ image }: { image?: Akira_protoServiceImage }) {
  if (!image) {
    return <Typography color="textSecondary">-</Typography>;
  }

  return (
    <Link
      color="textSecondary"
      underline="none"
      sx={{
        cursor: "pointer",
      }}
    >
      {image.name}@{image.version}
    </Link>
  );
}


type editProps = {
  client: ApiClient;
  onClose: () => void;
  onSubmit: SubmitHandler<EditServiceRequest>;
};

export function ServiceEditDrawer(props: editProps) {
  const { data: service } = useAspidaSWR(props.client?.services, {
    enabled: !!props.client,
  });
  const [searchParams] = useSearchParams();
  const serviceId = searchParams.get("id") as string;
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<EditServiceRequest>();
  return (
    <Drawer
      anchor="right"
      open={true}
      onClose={props.onClose}
      PaperProps={{ sx: { width: { sm: "100%", md: "40vw" } } }}
    >
      <Stack margin={2} spacing={2}>
        <Box>
          <Stack direction="row" alignItems="center">
            <IconButton onClick={props.onClose}>
              <CloseIcon />
            </IconButton>
            <Typography variant="h5" ml={1}>
              インスタンスの編集
            </Typography>
          </Stack>
          <Divider sx={{ mt: 1 }} />
        </Box>
        <Controller
          name="display_name"
          control={control}
          defaultValue="{service?.id}"
          rules={{
            required: ValidationMessages.Required,
          }}
          render={({ field }) => (
            <TextField
              {...field}
              label="表示名"
              variant="filled"
              error={!!errors.display_name}
              helperText={errors.display_name && errors.display_name.message}
            />
          )}
        />

        <Controller
          name="description"
          control={control}
          defaultValue=""
          render={({ field }) => (
            <TextField
              {...field}
              multiline
              rows={5}
              label="概要"
              variant="filled"
              fullWidth
              error={!!errors.description}
              helperText={errors.description && errors.description.message}
            />
          )}
        />
        <Button
          type="button"
          variant="contained"
          onClick={handleSubmit(props.onSubmit)}
        >
          変更
        </Button>
        <Button type="button" color="error" variant="outlined" onClick={props.onClose}>
          キャンセル
        </Button>
      </Stack>
    </Drawer>
  );
}

export function ServiceList(props: Props) {

function ServiceRow({
  service,
  onStart,
  onStop,
  onLaunch,
  onRemove
}: ServiceRowProps) {
  return (
    <>
      <TableRow sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
        <TableCell component="th" onClick={() => setEditDrawerOpened(true)}>
          {service.displayName}
        </TableCell>
        <TableCell>
            <ServiceImageLink image={service.image} />
        </TableCell>
        <TableCell>
          <Status status={service.status} />
        </TableCell>
        <TableCell align="right">
          {!!onLaunch && service.capabilities?.includes("open") ? (
            <IconButton
              onClick={() => onLaunch(service)}
              disabled={service.status !== "RUNNING"}
            >
              <LaunchIcon />
            </IconButton>
          ) : null}
          <PowerButton service={service} onStart={onStart} onStop={onStop} />
          {!!onRemove ? (
            <RemoveButton service={service} onRemove={onRemove} />
          ) : null}
        </TableCell>
      </TableRow>
    </>
  );
}
  
  const client = useApiClient();
  const { data, error, mutate } = useAspidaSWR(client?.services, {
    enabled: !!client,
    refreshInterval: 5 * 1000, // in ms
  });
  const setBusy = useSetBackdropValue();
  const [editDrawerOpened, setEditDrawerOpened] = useState(false);

  const onServiceEdit: SubmitHandler<EditServiceRequest> =
  useCallback(
    async (data) => {
      if (!client) return;

      // TODO: Handle error (e.g. Directory name conflicts)
      setBusy(true);
      try {
        await client.services.post({
          body: data,
        });
        setEditDrawerOpened(false);
        mutate();
      } finally {
        setBusy(false);
      }
    },
    [client, setBusy, setEditDrawerOpened, mutate]
  );
  
  const sortKey = useCallback(
    (lhs: Akira_protoService, rhs: Akira_protoService) => {
      const lhsStatus = lhs.status?.toString() ?? "";
      const rhsStatus = rhs.status?.toString() ?? "";
      if (lhsStatus === rhsStatus) {
        const lhsDisplayName = lhs.displayName ?? "";
        const rhsDisplayName = rhs.displayName ?? "";
        if (lhsDisplayName === rhsDisplayName) {
          return 0;
        } else if (lhsDisplayName > rhsDisplayName) {
          return 1;
        } else {
          return -1;
        }
      }

      return lhsStatus > rhsStatus ? 1 : -1;
    },
    []
  );
  return (
    <TableContainer component={Paper}>
    {editDrawerOpened ? (
      <ServiceEditDrawer
        client={client}
        onClose={() => {
          setEditDrawerOpened(false);
        }}
        onSubmit={onServiceEdit}
      />
    ) : (
      <></>
    )}
      <Table>
        <Header />
        <TableBody>
          {props.services?.sort(sortKey).map((x) => (
            <ServiceRow
              key={x.id}
              service={x}
              onStart={props.onStart}
              onStop={props.onStop}
              onLaunch={props.onLaunch}
              onRemove={props.onRemove}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
