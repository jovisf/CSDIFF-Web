import { ProductType } from "../types/types";

export enum Endpoints {
  beer = "beers",
  cart = "cart",
  cider = "cider",
  rating = "ratings",
}

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

export enum ProxiEndpoints {
  newPostCities = "http://localhost:3000/api/newPost/citiesLib",
  newPostSettlements = "http://localhost:3000/api/newPost/settlementsLib",
  geolocation = "http://localhost:3000/api/location",
  beer = "https://localhost:3000/api/products/beer",
  cart = "http://localhost:3000/api/cart",
  cartDB = "https://localhost:3000/api/cartDB",
  rating = "https://localhost:3000/api/rating",
}
