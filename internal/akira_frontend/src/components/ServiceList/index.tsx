import {
  IconButton,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { Akira_protoServiceStatus, Akira_protoService } from "../../api/@types";
import LaunchIcon from "@mui/icons-material/Launch";
import PowerSettingsNewIcon from "@mui/icons-material/PowerSettingsNew";
import DeleteIcon from "@mui/icons-material/Delete";
import { useCallback, useState } from "react";
import { PowerDialog, PowerDialogResult } from "./powerDialog";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { RemoveDialog, RemoveDialogResult } from "./removeDialog";

type Props = {
  services: Akira_protoService[];
  onStart: (target: Akira_protoService) => void;
  onStop: (target: Akira_protoService, terminate: boolean) => void;
  onLaunch: (target: Akira_protoService) => void;
  onRemove: (target: Akira_protoService) => void;
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
  const powerIcon =
    props.service.status === "RUNNING" ? (
      <PowerSettingsNewIcon color="error" />
    ) : (
      <PlayArrowIcon color="success" />
    );

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
  onLaunch: (target: Akira_protoService) => void;
  onRemove: (target: Akira_protoService) => void;
};

function ServiceRow({
  service,
  onStart,
  onStop,
  onLaunch,
  onRemove,
}: ServiceRowProps) {
  return (
    <>
      <TableRow sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
        <TableCell component="th">{service.displayName}</TableCell>
        <TableCell>
          <Link
            color="textSecondary"
            underline="none"
            sx={{
              cursor: "pointer",
            }}
          >
            {service.image?.name}@{service.image?.version}
          </Link>
        </TableCell>
        <TableCell>
          <Status status={service.status} />
        </TableCell>
        <TableCell align="right">
          <IconButton
            onClick={() => onLaunch(service)}
            disabled={service.status !== "RUNNING"}
          >
            <LaunchIcon />
          </IconButton>
          <PowerButton service={service} onStart={onStart} onStop={onStop} />
          <RemoveButton service={service} onRemove={onRemove} />
        </TableCell>
      </TableRow>
    </>
  );
}

export function ServiceList(props: Props) {
  return (
    <TableContainer component={Paper}>
      <Table>
        <Header />
        <TableBody>
          {props.services?.map((x) => (
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
