import { TableCell, TableRow, IconButton, Table } from "@mui/material";
import { Akira_protoProject } from "../../api/@types";
import LaunchIcon from "@mui/icons-material/Launch";
import { Link } from "react-router-dom";
import { RemoveButton } from "../../components/RemoveProjectButton";
import { ApiClient } from "../../hooks/api";

type Props = {
  project: Akira_protoProject;
  client: ApiClient;
  onRemove: (target: Akira_protoProject) => void;
};

export function ProjectListHeader() {
  return (
    <Table width="100%">
      <TableRow>
        <TableCell sx={{ width: "20%" }}>プロジェクト名</TableCell>
        <TableCell sx={{ width: "20%" }}>作者名</TableCell>
        <TableCell sx={{ width: "40%" }}>概要</TableCell>
        <TableCell sx={{ width: "20%" }}></TableCell>
      </TableRow>
    </Table>
  );
}
export function ProjectListItem({ project, client, onRemove }: Props) {
  return (
    <Table width="100%">
      <TableRow
        sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
        style={{ height: 20 }}
      >
        <TableCell sx={{ width: "20%" }}>
          <Link to={`/projects/details?id=${project.id}`}>
            {project.manifest?.name}
          </Link>
        </TableCell>
        <TableCell sx={{ width: "20%" }}> {project.manifest?.author}</TableCell>
        <TableCell sx={{ width: "40%" }}>
          {project.manifest?.description}
        </TableCell>
        <TableCell sx={{ width: "20%" }}>
          <IconButton component={Link} to="/services">
            <LaunchIcon />
          </IconButton>
          <RemoveButton project={project} client={client} onRemove={onRemove} />
        </TableCell>
      </TableRow>
    </Table>
  );
}
