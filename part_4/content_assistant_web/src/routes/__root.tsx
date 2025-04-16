import { createRootRoute, Link, Outlet } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools';

export const Route = createRootRoute({
  component: () => (
    <>
      <div className="bg-violet-500 h-16">
        <div className="container mx-auto flex justify-between gap-2 items-center font-light h-full text-white">
          <Link to="/workflows" className="text-xl font-bold">
            Content Creator
          </Link>
          <div className="flex justify-between h-full items-center">
            <Link
              to="/workflows"
              className="[&.active]:font-bold px-2 hover:bg-violet-700 h-full flex items-center cursor-pointer text-white"
            >
              Workflows
            </Link>{' '}
            <Link
              to="/blogs"
              className="[&.active]:font-bold px-2 hover:bg-violet-700 h-full flex items-center cursor-pointer"
            >
              Blogs
            </Link>
            <Link
              to="/social_media"
              className="[&.active]:font-bold px-2 h-full hover:bg-violet-700 flex items-center cursor-pointer"
            >
              Social Media
            </Link>
          </div>
        </div>
      </div>
      <Outlet />
      <TanStackRouterDevtools />
    </>
  ),
});
