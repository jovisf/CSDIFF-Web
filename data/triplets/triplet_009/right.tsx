'use client';
import { useSearchParams } from 'next/navigation';
import { Suspense, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import CartModal from '../../ui/modals/CartModal';

export default function Portal() {
  const [element, setElement] = useState<HTMLBodyElement | null>(null);

  const searchParams = useSearchParams();
  const modal = searchParams.get('cart');
  useEffect(() => {
    setElement(document.querySelector('body'));
  }, []);
  return modal && element && createPortal(<CartModal />, element);
}
