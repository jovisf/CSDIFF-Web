import { ProductType } from '../types/types';

export enum Endpoints {
  beer = 'beers',
  cart = 'cart',
  cider = 'cider',
  rating = 'ratings',
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
  newPostCities = 'https://hop-oasis-fr.vercel.app/api/newPost/citiesLib',
  newPostSettlements = 'https://hop-oasis-fr.vercel.app/api/newPost/settlementsLib',
  geolocation = 'https://hop-oasis-fr.vercel.app/api/location',
  beer = 'https://hop-oasis-fr.vercel.app/api/products/beer',
  cart = 'https://hop-oasis-fr.vercel.app/api/cart',
  cartDB = 'https://hop-oasis-fr.vercel.app/api/cartDB',
  rating = 'https://hop-oasis-fr.vercel.app/api/rating',
}
