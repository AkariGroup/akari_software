import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

export enum PowerDialogResult {
  CANCEL = 0,
  SHUTDOWN = 1,
  TERMINATE = 2,
}

type Props = {
  serviceName: string;
  onResponse: (d: PowerDialogResult) => void;
};

export function PowerDialog(props: Props) {
  return (
    <Dialog
      open={true}
      onClose={() => props.onResponse(PowerDialogResult.CANCEL)}
    >
      <DialogTitle>確認</DialogTitle>
      <DialogContent>
        <DialogContentText>
          '{props.serviceName}' をシャットダウンしますか？
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => props.onResponse(PowerDialogResult.CANCEL)}>
          キャンセル
        </Button>
        <Button
          onClick={() => props.onResponse(PowerDialogResult.SHUTDOWN)}
          color="error"
        >
          停止
        </Button>
        <Button
          onClick={() => props.onResponse(PowerDialogResult.TERMINATE)}
          color="error"
        >
          完全停止
        </Button>
      </DialogActions>
    </Dialog>
  );
}
