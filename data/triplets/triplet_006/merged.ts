import { ProductType } from "../types/types";

export interface IPropsGet {
  endpoint: Endpoints;
}

export interface IPropsGetById extends IPropsGet {
  id: string;
}

export interface IPropsGetById {
  endpoint: Endpoints;
  id: string;
}

export type CartResponseType = {
  items: ProductType[];
  priceForAll: number;
};

export type PageableType = {
  pageNumber: number;
  pageSize: number;
  sort: {
    empty: boolean;
    sorted: boolean;
    unsorted: boolean;
  };
  offset: number;
  paged: boolean;
  unpaged: boolean;
};

export type ProductsResponseType = {
  content: ProductType[];
  pageable: PageableType;
  totalElements: number;
  totalPages: number;
  last: boolean;
  size: number;
  number: number;
  sort: {
    empty: boolean;
    sorted: boolean;
    unsorted: boolean;
  };
  numberOfElements: number;
  first: boolean;
  empty: boolean;
};

const proxiUrl = process.env.HOST_URL;
const apiUrl = process.env.API_URL;

export enum Endpoints {
  beer = "beers",
  cart = "cart",
  cider = "cider",
  rating = "ratings",
}

export const ProxiEndpoints = {
  beer: proxiUrl + "products/" + Endpoints.beer,
  cart: proxiUrl + Endpoints.cart,
  rating: proxiUrl + Endpoints.rating,
  //future remove
  cartDB: proxiUrl + "cartDB",
};

export const ApiEndpoints = {
  beer: apiUrl + Endpoints.beer,
  cart: apiUrl + Endpoints.cart,
  rating: apiUrl + Endpoints.rating,
};
