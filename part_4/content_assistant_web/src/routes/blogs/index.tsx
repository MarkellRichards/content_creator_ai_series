import { useState } from 'react';
import { createFileRoute } from '@tanstack/react-router';
import { blogsQueryOptions } from '../../services/blog_postsQueryOptions';
import { useSuspenseQuery } from '@tanstack/react-query';
import BlogCard from '../../components/blog/blog';
import Pagination from '../../components/pagination/pagination';

export const Route = createFileRoute('/blogs/')({
  component: RouteComponent,
  // @ts-ignore
  // loader: ({ context: { queryClient } }) =>
  //   queryClient.ensureQueryData(blogsQueryOptions),
  loader: ({ context: { queryClient }, params: { offset, limit } }) =>
    queryClient.ensureQueryData(blogsQueryOptions(offset, limit)),
});

function RouteComponent() {
  const [offset, setOffset] = useState(0);
  const LIMIT = 5;

  const blogsQuery = useSuspenseQuery(blogsQueryOptions(offset, LIMIT));
  // const blogsQuery = useSuspenseQuery(blogsQueryOptions(offset, LIMIT));
  const blogs = blogsQuery.data.blogs;
  const total = blogsQuery.data.total;
  return (
    <div className="container mx-auto my-8 flex flex-col">
      <div className="mb-8 text-center text-2xl font-bold">Your Blogs</div>
      <ul className="grid lg:grid-cols-4 sm:grid-cols-1 gap-8 container mx-auto">
        {[...blogs].map((blog, index) => {
          return (
            <li key={index} className="whitespace-nowrap">
              <BlogCard blog={blog} />
            </li>
          );
        })}
      </ul>
      <Pagination
        total={total}
        offset={offset}
        limit={LIMIT}
        setOffset={setOffset}
      />
      {/* <Outlet /> */}
    </div>
  );
}
