import { TableCell, TableRow, IconButton } from "@mui/material";
import { Akira_protoProject } from "../../api/@types";
import FavoriteIcon from "@mui/icons-material/Favorite";
import DeleteIcon from "@mui/icons-material/Delete";
import LaunchIcon from "@mui/icons-material/Launch";
import { Link } from "react-router-dom";
import MoreVertIcon from "@mui/icons-material/MoreVert";

type Prop = {
  project: Akira_protoProject;
};

export function ProjectList({ project }: Prop) {
  return (
    <TableRow
      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
      style={{ height: 20 }}
    >
      <TableCell sx={{ width: 300 }}>
        <Link to={`/projects/details?id=${project.id}`}>
          {project.manifest?.name}
        </Link>
      </TableCell>
      <TableCell sx={{ width: 300 }}> {project.manifest?.author}</TableCell>
      <TableCell sx={{ width: 600 }}>
        {project.manifest?.description}
      </TableCell>
      <TableCell sx={{ width: 200 }}>
        <IconButton disabled>
          <FavoriteIcon />
        </IconButton>
        <IconButton component={Link} to="/services">
          <LaunchIcon />
        </IconButton>
        <IconButton disabled>
          <DeleteIcon />
        </IconButton>
        <IconButton sx={{ marginLeft: "auto" }}>
          <MoreVertIcon />
        </IconButton>
      </TableCell>
    </TableRow>
  );
}
