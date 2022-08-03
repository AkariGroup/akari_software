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
import {
  Akira_protoInstanceStatus,
  Akira_protoServiceInstance,
} from "../../api/@types";
import LaunchIcon from "@mui/icons-material/Launch";
import PowerSettingsNewIcon from "@mui/icons-material/PowerSettingsNew";
import DeleteIcon from "@mui/icons-material/Delete";
import { useCallback, useState } from "react";
import { PowerDialog, PowerDialogResult } from "./powerDialog";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { RemoveDialog, RemoveDialogResult } from "./removeDialog";

type Props = {
  instances: Akira_protoServiceInstance[];
  onStart: (target: Akira_protoServiceInstance) => void;
  onStop: (target: Akira_protoServiceInstance, terminate: boolean) => void;
  onLaunch: (target: Akira_protoServiceInstance) => void;
  onRemove: (target: Akira_protoServiceInstance) => void;
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

function Status({ status }: { status?: Akira_protoInstanceStatus }) {
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
  instance: Akira_protoServiceInstance;
  onStart: (target: Akira_protoServiceInstance) => void;
  onStop: (target: Akira_protoServiceInstance, terminate: boolean) => void;
};

function PowerButton(props: PowerButtonProps) {
  const [powerDialogOpened, setPowerDialogOpened] = useState(false);
  const onPowerIconClicked = useCallback(() => {
    if (props.instance.status === "RUNNING") {
      setPowerDialogOpened(true);
    } else {
      props.onStart(props.instance);
    }
  }, [props, setPowerDialogOpened]);
  const onPowerConfirmation = useCallback(
    (d: PowerDialogResult) => {
      setPowerDialogOpened(false);
      if (d === PowerDialogResult.CANCEL) {
        return;
      } else {
        props.onStop(props.instance, d === PowerDialogResult.TERMINATE);
      }
    },
    [props, setPowerDialogOpened]
  );
  const powerButtonDisabled =
    props.instance.status === "STARTING" ||
    props.instance.status === "STOPPING";
  const powerIcon =
    props.instance.status === "RUNNING" ? (
      <PowerSettingsNewIcon color="error" />
    ) : (
      <PlayArrowIcon color="success" />
    );

  return (
    <>
      {powerDialogOpened ? (
        <PowerDialog
          serviceName={props.instance.displayName ?? ""}
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
  instance: Akira_protoServiceInstance;
  onRemove: (target: Akira_protoServiceInstance) => void;
};

function RemoveButton(props: RemoveButtonProps) {
  const [opened, setOpened] = useState(false);
  const onConfirm = useCallback(
    (d: RemoveDialogResult) => {
      setOpened(false);
      if (d === RemoveDialogResult.CANCEL) {
        return;
      } else {
        props.onRemove(props.instance);
      }
    },
    [props, setOpened]
  );
  return (
    <>
      {opened ? (
        <RemoveDialog
          serviceName={props.instance.displayName ?? ""}
          onResponse={onConfirm}
        />
      ) : null}
      <IconButton onClick={() => setOpened(true)}>
        <DeleteIcon />
      </IconButton>
    </>
  );
}

type InstanceProp = {
  instance: Akira_protoServiceInstance;
  onStart: (target: Akira_protoServiceInstance) => void;
  onStop: (target: Akira_protoServiceInstance, terminate: boolean) => void;
  onLaunch: (target: Akira_protoServiceInstance) => void;
  onRemove: (target: Akira_protoServiceInstance) => void;
};

function InstanceRow({
  instance,
  onStart,
  onStop,
  onLaunch,
  onRemove,
}: InstanceProp) {
  return (
    <>
      <TableRow sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
        <TableCell component="th">{instance.displayName}</TableCell>
        <TableCell>
          <Link
            color="textSecondary"
            underline="none"
            sx={{
              cursor: "pointer",
            }}
          >
            {instance.service?.name}@{instance.service?.version}
          </Link>
        </TableCell>
        <TableCell>
          <Status status={instance.status} />
        </TableCell>
        <TableCell align="right">
          <IconButton
            onClick={() => onLaunch(instance)}
            disabled={instance.status !== "RUNNING"}
          >
            <LaunchIcon />
          </IconButton>
          <PowerButton instance={instance} onStart={onStart} onStop={onStop} />
          <RemoveButton instance={instance} onRemove={onRemove} />
        </TableCell>
      </TableRow>
    </>
  );
}

export function InstanceList(props: Props) {
  return (
    <TableContainer component={Paper}>
      <Table>
        <Header />
        <TableBody>
          {props.instances?.map((x) => (
            <InstanceRow
              key={x.id}
              instance={x}
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
