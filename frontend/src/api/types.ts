import type { ItemStatus, ItemTypes } from "./enums";

export interface IUser {
  id: number;
  email: string;
  name: string;
  permissions: number;
}

export interface IItem {
  id: number;
  user_id: number;
  name: string;
  type: ItemTypes;
  created_at: string;
  description: string;
  status: ItemStatus;
  image_url: string;
}

export interface ICreateItem {
  name: string;
  type: ItemTypes;
  description: string;
  image: File;
}

export interface IUpdateItem {
  name: string;
  type: ItemTypes;
  description: string;
  status: ItemStatus;
}
