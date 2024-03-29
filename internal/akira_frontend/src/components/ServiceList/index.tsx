import {
  CircularProgress,
  IconButton,
  Link,
  Paper,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { Link as MuiLink } from "react-router-dom";
import {
  Akira_protoServiceState,
  Akira_protoService,
  Akira_protoServiceImage,
} from "../../api/@types";
import LaunchIcon from "@mui/icons-material/Launch";
import PowerSettingsNewIcon from "@mui/icons-material/PowerSettingsNew";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { useCallback, useState } from "react";
import { PowerDialog, PowerDialogResult } from "./powerDialog";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { RemoveDialog, RemoveDialogResult } from "./removeDialog";
import PreviewIcon from "@mui/icons-material/Preview";

type Props = {
  services: Akira_protoService[];
  onStart: (target: Akira_protoService) => void;
  onStop: (target: Akira_protoService, terminate: boolean) => void;
  onTerminate: (target: Akira_protoService) => void;
  onLaunch?: (target: Akira_protoService) => void;
  onRemove?: (target: Akira_protoService) => void;
  onEdit?: (target: Akira_protoService) => void;
  onAutoStart: (target: Akira_protoService) => void;
};

function Header() {
  return (
    <TableHead>
      <TableRow>
        <TableCell width="20%">DisplayName</TableCell>
        <TableCell width="30%">Service</TableCell>
        <TableCell width="20%">State</TableCell>
        <TableCell width="10%">AutoStart</TableCell>
        <TableCell width="20%"></TableCell>
      </TableRow>
    </TableHead>
  );
}

function State({ state }: { state?: Akira_protoServiceState }) {
  let color = "primary";
  let bold = false;
  switch (state) {
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
      {state === "STARTING" ? "STARTING / UPDATING" : state}
    </Typography>
  );
}

type PowerButtonProps = {
  service: Akira_protoService;
  onStart: (target: Akira_protoService) => void;
  onStop: (target: Akira_protoService, terminate: boolean) => void;
  onTerminate: (target: Akira_protoService) => void;
};

function PowerButton(props: PowerButtonProps) {
  const [powerDialogOpened, setPowerDialogOpened] = useState(false);
  const onPowerIconClicked = useCallback(() => {
    if (props.service.state === "RUNNING") {
      setPowerDialogOpened(true);
    } else if (props.service.state === "ERROR") {
      props.onTerminate(props.service);
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
    props.service.state === "STARTING" || props.service.state === "STOPPING";
  const powerIcon = (() => {
    if (powerButtonDisabled) {
      return <CircularProgress />;
    } else if (props.service.state === "ERROR") {
      return <PowerSettingsNewIcon color="secondary" />;
    } else if (props.service.state === "RUNNING") {
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
  onTerminate: (target: Akira_protoService) => void;
  onLaunch?: (target: Akira_protoService) => void;
  onRemove?: (target: Akira_protoService) => void;
  onEdit?: (target: Akira_protoService) => void;
  onAutoStart?: (target: Akira_protoService) => void;
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

function ServiceRow({
  service,
  onStart,
  onStop,
  onLaunch,
  onRemove,
  onEdit,
  onAutoStart,
  onTerminate,
}: ServiceRowProps) {
  return (
    <>
      <TableRow sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
        <TableCell
          style={{ textDecoration: "underline" }}
          component="th"
          onClick={() => onEdit?.(service)}
        >
          {service.displayName}
        </TableCell>
        <TableCell>
          <ServiceImageLink image={service.image} />
        </TableCell>
        <TableCell>
          <State state={service.state} />
        </TableCell>
        <TableCell>
          <Switch
            checked={service.autoStart}
            onChange={() => onAutoStart?.(service)}
          />
        </TableCell>
        <TableCell align="right">
          {!!onEdit ? (
            <IconButton onClick={() => onEdit(service)}>
              <EditIcon />
            </IconButton>
          ) : null}
          {!!onLaunch && service.capabilities?.includes("open") ? (
            <IconButton
              onClick={() => onLaunch(service)}
              disabled={service.state !== "RUNNING"}
            >
              <LaunchIcon />
            </IconButton>
          ) : null}
          <PowerButton
            service={service}
            onStart={onStart}
            onStop={onStop}
            onTerminate={onTerminate}
          />
          {!!onRemove ? (
            <RemoveButton service={service} onRemove={onRemove} />
          ) : null}
          <IconButton component={MuiLink} to={`/services/logs/${service.id}`}>
            <PreviewIcon />
          </IconButton>
        </TableCell>
      </TableRow>
    </>
  );
}

export function ServiceList(props: Props) {
  const sortKey = useCallback(
    (lhs: Akira_protoService, rhs: Akira_protoService) => {
      const lhsState = lhs.state?.toString() ?? "";
      const rhsState = rhs.state?.toString() ?? "";
      if (lhsState === rhsState) {
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

      return lhsState > rhsState ? 1 : -1;
    },
    []
  );
  return (
    <TableContainer component={Paper}>
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
              onEdit={props.onEdit}
              onAutoStart={props.onAutoStart}
              onTerminate={props.onTerminate}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
