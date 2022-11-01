import {
  TypedUseSelectorHook,
  useDispatch as useDispatch_,
  useSelector as useSelector_,
} from "react-redux";
import { State, Dispatch } from "./types";

export const useDispatch = () => useDispatch_<Dispatch>();
export const useSelector: TypedUseSelectorHook<State> = useSelector_;
