import { createFileRoute, Link } from '@tanstack/react-router';
import { workflowsQueryOptions } from '../../services/workflowsQueryOptions';
import { useSuspenseQuery } from '@tanstack/react-query';
import { useState } from 'react';
import Pagination from '../../components/pagination/pagination';

export const Route = createFileRoute('/workflows/')({
  component: RouteComponent,
  loader: ({
    // @ts-ignore
    context: { queryClient },
    // @ts-ignore
    params: { offset, limit, filter_criteria },
  }) =>
    queryClient.ensureQueryData(
      workflowsQueryOptions(offset, limit, filter_criteria),
    ),
});

function RouteComponent() {
  const [offset, setOffset] = useState(0);
  const [filterCriteria, setFilterCriteria] = useState({ status: 'COMPLETE' });
  const LIMIT = 10;
  const workflowsQuery = useSuspenseQuery(
    // @ts-ignore
    workflowsQueryOptions(offset, LIMIT, filterCriteria),
  );
  const workflows = workflowsQuery.data.workflows;
  const total = workflowsQuery.data.total;

  const handleFilterChange = (newFilter: string) => {
    setFilterCriteria({ status: newFilter });
    setOffset(0);
  };

  return (
    <div className="container mx-auto my-8 flex flex-col">
      <div className="mb-8 text-center text-2xl font-bold">Your Workflows</div>
      <div className="w-full flex lg:justify-end mb-4">
        <Link to="/workflows/create">
          <button className="p-4 bg-violet-500 hover:bg-violet-700 text-white rounded-b-sm cursor-pointer">
            Create Workfow
          </button>
        </Link>
      </div>
      <div className="flex lg:justify-end mb-4">
        <div className="flex justify-between">
          <label htmlFor="statusFilter" className="mr- py-1">
            Filter by status:
          </label>
          <select
            id="statusFilter"
            value={filterCriteria.status}
            onChange={(e) => handleFilterChange(e.target.value)}
            className=" rounded py-1 px-2 outline-violet-500"
          >
            <option value="COMPLETE">Complete</option>
            <option value="FAILED">Failed</option>
            <option value="INPROGRESS">In Progress</option>
          </select>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Timestamp
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Details
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {workflows.map((item, index) => (
              <tr key={index}>
                <td className="px-6 py-4">{item.status}</td>
                <td className="px-6 py-4">
                  {new Date(item.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4">
                  <Link
                    to="/workflows/$workflowId"
                    params={{ workflowId: item.guid }}
                    className="text-violet-500 hover:underline"
                  >
                    View Details
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Pagination
        total={total}
        offset={offset}
        limit={LIMIT}
        setOffset={setOffset}
      />
    </div>
  );
}
