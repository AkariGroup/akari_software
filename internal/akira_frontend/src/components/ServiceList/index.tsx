import {
  CircularProgress,
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
  Akira_protoServiceStatus,
  Akira_protoService,
  Akira_protoServiceImage,
} from "../../api/@types";
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

export function ServiceList(props: Props) {
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
