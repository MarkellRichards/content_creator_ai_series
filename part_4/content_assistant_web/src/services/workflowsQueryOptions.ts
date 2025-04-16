import { queryOptions } from "@tanstack/react-query";
import { fetchWorkflow, fetchWorkflows, FilterCriteria } from "./workflows";

export const workflowsQueryOptions = (offset: number, limit: number, filter_criteria?: FilterCriteria) => queryOptions({
    queryKey: ['workflows', offset, limit, filter_criteria],
    // @ts-ignore
    queryFn: () => fetchWorkflows(offset, limit, filter_criteria)
})

export const workflowQueryOptions = (workflow_guid: string) => queryOptions({
    queryKey: ['workflow', {workflow_guid}],
    queryFn: () => fetchWorkflow(workflow_guid)
})