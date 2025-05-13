import { createRootRoute, Outlet } from '@tanstack/react-router';
import Navbar from '../components/shared/navigation/navbar';

export const Route = createRootRoute({
  component: () => (
    <>
      <Navbar />
      <Outlet />
    </>
  ),
});
