import {
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
import { PowerDialog, DialogResult } from "./powerDialog";

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

type InstanceProp = {
  instance: Akira_protoServiceInstance;
  onStart: (target: Akira_protoServiceInstance) => void;
  onStop: (target: Akira_protoServiceInstance, terminate: boolean) => void;
  onLaunch: (target: Akira_protoServiceInstance) => void;
  onRemove: (target: Akira_protoServiceInstance) => void;
};

function PowerButton(props: InstanceProp) {
  const [powerDialogOpened, setPowerDialogOpened] = useState(false);
  const onPowerIconClicked = useCallback(() => {
    if (props.instance.status === "RUNNING") {
      setPowerDialogOpened(true);
    } else {
      props.onStart(props.instance);
    }
  }, [props, setPowerDialogOpened]);
  const onPowerConfirmation = useCallback(
    (d: DialogResult) => {
      setPowerDialogOpened(false);
      if (d === DialogResult.CANCEL) {
        return;
      } else {
        props.onStop(props.instance, d === DialogResult.TERMINATE);
      }
    },
    [props, setPowerDialogOpened]
  );
  const powerButtonDisabled =
    props.instance.status === "STARTING" ||
    props.instance.status === "STOPPING";
  const powerButtonOff = props.instance.status === "RUNNING";

  return (
    <>
      {powerDialogOpened ? (
        <PowerDialog onResponse={onPowerConfirmation} />
      ) : null}
      <IconButton onClick={onPowerIconClicked} disabled={powerButtonDisabled}>
        <PowerSettingsNewIcon color={powerButtonOff ? "error" : "success"} />
      </IconButton>
    </>
  );
}

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
          <IconButton onClick={() => onLaunch(instance)}>
            <LaunchIcon />
          </IconButton>
          <PowerButton
            instance={instance}
            onStart={onStart}
            onStop={onStop}
            onLaunch={onLaunch}
            onRemove={onRemove}
          />
          <IconButton onClick={() => onRemove(instance)}>
            <DeleteIcon />
          </IconButton>
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
