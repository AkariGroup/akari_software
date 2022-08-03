import { Alert, AlertTitle } from "@mui/material";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

export enum RemoveDialogResult {
  CANCEL = 0,
  CONTINUE = 1,
}

type Props = {
  serviceName: string;
  onResponse: (d: RemoveDialogResult) => void;
};

export function RemoveDialog(props: Props) {
  return (
    <Dialog
      open={true}
      onClose={() => props.onResponse(RemoveDialogResult.CANCEL)}
    >
      <DialogTitle>確認</DialogTitle>
      <DialogContent>
        <DialogContentText>
          '{props.serviceName}' を削除しますか？
          <Alert severity="error" sx={{ mt: 1, mb: 1 }}>
            <AlertTitle>警告</AlertTitle>
            この操作は <strong>取り消すことができません</strong>
          </Alert>
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => props.onResponse(RemoveDialogResult.CANCEL)}>
          キャンセル
        </Button>
        <Button
          onClick={() => props.onResponse(RemoveDialogResult.CONTINUE)}
          color="error"
        >
          削除
        </Button>
      </DialogActions>
    </Dialog>
  );
}
