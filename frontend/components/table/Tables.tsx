import React, { useEffect, useState, useMemo, useCallback } from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Input,
  Button,
  DropdownTrigger,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Chip,
  Pagination,
} from "@nextui-org/react";
import { PlusIcon } from "./PulseIcon";
import {
  FiMoreVertical as VerticalDotsIcon,
  FiSearch as SearchIcon,
  FiChevronDown as ChevronDownIcon,
} from "react-icons/fi";
import { makeRequest } from "@/request";

// Define types for columns and products
interface IProduct {
  id: string;
  name: string;
  quantity: number;
  price_per_unit: number;
  category: string;
  description: string;
  created_at: Date;
  status: "available" | "out_of_stock" | "discontinued";
}

// Define the structure of a column
interface Column {
  uid: string;
  name: string;
  sortable?: boolean;
}

const statusOptions = [
  { uid: "available", name: "Available" },
  { uid: "out_of_stock", name: "Out of stock" },
  { uid: "discontinued", name: "Discontinued" },
];

const columns: Column[] = [
  // { uid: "id", name: "ID", sortable: false },
  { uid: "name", name: "Name", sortable: true },
  { uid: "quantity", name: "Quantity", sortable: true },
  { uid: "price_per_unit", name: "Price Per Unit", sortable: true },
  { uid: "category", name: "Category", sortable: true },
  { uid: "description", name: "Description" },
  { uid: "created_at", name: "Created At", sortable: true },
  { uid: "status", name: "Status", sortable: true },
  { uid: "actions", name: "Actions" }
];

const statusColorMap: Record<string, "available" | "out_of_stock" | "discontinued"> = {
  available: "available",
  out_of_stock: "out_of_stock",
  discontinued: "discontinued",
};

const INITIAL_VISIBLE_COLUMNS = ["id", "name", "quantity", "price_per_unit", "category", "actions"];

export default function Tables() {
  const [filterValue, setFilterValue] = useState<string>("");
  const [selectedKeys, setSelectedKeys] = useState<Set<React.Key>>(new Set([]));
  const [visibleColumns, setVisibleColumns] = useState<Set<string>>(new Set(INITIAL_VISIBLE_COLUMNS));
  const [statusFilter, setStatusFilter] = useState<Set<string>>(new Set(["all", "available"]));
  const [rowsPerPage, setRowsPerPage] = useState<number>(5);
  const [product, setProduct] = useState<IProduct[] | null>(null);
  const [sortDescriptor, setSortDescriptor] = useState<{ column: string; direction: "ascending" | "descending" }>({
    column: "name",
    direction: "ascending",
  });
  const [page, setPage] = useState<number>(1);
  const hasSearchFilter = Boolean(filterValue);


  const headerColumns = useMemo(() => {
    if (visibleColumns.size === 0) return columns;
    return columns.filter((column) => visibleColumns.has(column.uid));
  }, [visibleColumns]);

  const filteredItems = useMemo(() => {
    let filteredProducts = product !== null ? product : [];

    if (hasSearchFilter) {
      filteredProducts = filteredProducts.filter((p) =>
        p.name.toLowerCase().includes(filterValue.toLowerCase())
      );
    }
    if (!statusFilter.has("all")) {
      filteredProducts = filteredProducts.filter((p) => statusFilter.has(p.status));
    }

    if (Array.from(statusFilter).length !== statusOptions.length) {

      filteredProducts = filteredProducts.filter((p) =>
        Array.from(statusFilter).includes(p.status),
      );
    }

    return filteredProducts;
  }, [product, filterValue, statusFilter]);

  const pages = Math.ceil(filteredItems.length / rowsPerPage);

  const items = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    return filteredItems.slice(start, end);
  }, [page, filteredItems, rowsPerPage]);

  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => {
      const first = a[sortDescriptor.column as keyof IProduct];
      const second = b[sortDescriptor.column as keyof IProduct];
      const cmp = first < second ? -1 : first > second ? 1 : 0;
      return sortDescriptor.direction === "descending" ? -cmp : cmp;
    });
  }, [sortDescriptor, items]);

  const classNames = useMemo(
    () => ({
      wrapper: ["max-h-[382px]", "max-w-4/5", "twraper", "product-table"],
      th: ["bg-transparent", "text-default-500", "border-b", "border-divider"],
      td: [
        "group-data-[first=true]:first:before:rounded-none",
        "group-data-[first=true]:last:before:rounded-none",
        "group-data-[middle=true]:before:rounded-none",
        "group-data-[last=true]:first:before:rounded-none",
        "group-data-[last=true]:last:before:rounded-none",
      ],
    }),
    []
  );

  const fetchProduct = async () => {
    await makeRequest('product', null, (err: any, data: any) => {
      if (err) return console.error(err);
      setProduct(data.data);
    }, "GET");
  }

  useEffect(() => {
    fetchProduct();
  }, []);

  const renderCell = useCallback((product: IProduct, columnKey: string) => {
    const cellValue = product[columnKey as keyof IProduct];

    switch (columnKey) {
      case "status":
        return (
          <Chip className="capitalize" color={statusColorMap[product.status]} size="sm" variant="flat">
            {cellValue as string}
          </Chip>
        );
      case "actions":
        return (
          <div className="relative flex justify-end items-center gap-2">
            <Dropdown>
              <DropdownTrigger>
                <Button isIconOnly size="sm" variant="light">
                  <VerticalDotsIcon className="text-default-300" />
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                style={{ width: '100%', background: '#333', color: '#fff', boxShadow: '0 0 6px 0', padding: '0 5px', borderRadius: '4px', display: 'flex' }}
              >
                <DropdownItem>View</DropdownItem>
                <DropdownItem>Edit</DropdownItem>
                <DropdownItem>Delete</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </div>
        );
      default:
        return cellValue;
    }
  }, []);

  const onNextPage = useCallback(() => {
    if (page < pages) {
      setPage(page + 1);
    }
  }, [page, pages]);

  const onPreviousPage = useCallback(() => {
    if (page > 1) {
      setPage(page - 1);
    }
  }, [page]);

  const onRowsPerPageChange = useCallback((e: React.ChangeEvent<HTMLSelectElement>) => {
    setRowsPerPage(Number(e.target.value));
    setPage(1);
  }, []);

  const onSearchChange = useCallback((value: string) => {
    setFilterValue(value);
    setPage(1);
  }, []);

  const onClear = useCallback(() => {
    setFilterValue("");
    setPage(1);
  }, []);

  const onStatusChange = useCallback((keys: Set<string>) => {
    console.log(keys, "keys")
    setStatusFilter(keys);
    setPage(1);
  }, []);

  const capitalize = (str: string): string => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  const topContent = useMemo(() => {
    return (
      <div className="flex flex-col gap-4">
        <div className="flex justify-between gap-3 items-end">
          <Input
            style={{ width: "100%", height: "42px", border: "1px solid #fff", borderRadius: "7px", fontSize: "15.5px", padding: "0 2em" }}
            isClearable
            className="w-full sm:max-w-[44%]"
            placeholder="Search by name..."
            startContent={<SearchIcon style={{ position: "absolute", fontSize: "31px", top: "5px", left: "2px" }} />}
            value={filterValue}
            onClear={onClear}
            onValueChange={onSearchChange}
          />
          <div className="flex gap-3 after-search">
            <Dropdown>
              <DropdownTrigger className="hidden sm:flex">
                <Button endContent={<ChevronDownIcon className="text-small" />} variant="flat">
                  Status
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                disallowEmptySelection
                aria-label="Status Filter"
                closeOnSelect={false}
                selectedKeys={statusFilter}
                selectionMode="multiple"
                onSelectionChange={onStatusChange}
                style={{ width: '100%', background: '#333', color: '#fff', boxShadow: '0 0 6px 0', padding: '0 5px', borderRadius: '4px', display: 'flex' }}
              >
                {statusOptions.map((status) => (
                  <DropdownItem key={status.uid} className="capitalize">
                    {capitalize(status.name)}
                  </DropdownItem>
                ))}
              </DropdownMenu>
            </Dropdown>
            <Dropdown>
              <DropdownTrigger className="hidden sm:flex">
                <Button endContent={<ChevronDownIcon className="text-small" />} variant="flat">
                  Columns
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                disallowEmptySelection
                aria-label="Table Columns"
                closeOnSelect={false}
                selectedKeys={visibleColumns}
                selectionMode="multiple"
                onSelectionChange={(keys) => setVisibleColumns(new Set(keys as Set<string>))}
                style={{ width: '100%', background: '#333', color: '#fff', boxShadow: '0 0 6px 0', padding: '0 5px', borderRadius: '4px', display: 'flex' }}
              >
                {columns.map((column) => (
                  <DropdownItem key={column.uid} className="capitalize">
                    {capitalize(column.name)}
                  </DropdownItem>
                ))}
              </DropdownMenu>
            </Dropdown>
            <Button color="primary" endContent={<PlusIcon />}>
              Add New
            </Button>
          </div>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-default-400 text-small">Total {product ? product.length : 0} products</span>
          <label className="flex items-center text-default-400 text-small">
            Rows per page:
            <select className="bg-transparent outline-none text-default-400 text-small" style={{ width: '100%', background: '#333', color: '#fff', boxShadow: '0 0 6px 0', padding: '0 5px', borderRadius: '4px', display: 'flex' }} onChange={onRowsPerPageChange}>
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
            </select>
          </label>
        </div>
      </div>
    );
  }, [filterValue, statusFilter, visibleColumns, onRowsPerPageChange, product ? product.length : 0, onSearchChange, hasSearchFilter]);

  const bottomContent = useMemo(() => {
    return (
      <div className="py-2 px-2 flex justify-between items-center">
        <span className="w-[30%] text-small text-default-400">
          {selectedKeys.size === (product ? product.length : 0)
            ? "All items selected"
            : `${selectedKeys.size} of ${filteredItems.length} selected`}
        </span>
        <Pagination isCompact showControls showShadow color="primary" page={page} total={pages} onChange={setPage} />
        <div className="hidden sm:flex w-[30%] justify-end gap-2">
          <Button isDisabled={page === 1} size="sm" variant="flat" onPress={onPreviousPage}>
            Previous
          </Button>
          <Button isDisabled={page === pages} size="sm" variant="flat" onPress={onNextPage}>
            Next
          </Button>
        </div>
      </div>
    );
  }, [selectedKeys, items.length, page, pages, hasSearchFilter, product]);

  return (
    product && (
      <div className="flex w-[90%]">
        <Table
          aria-label="Example table with custom cells, pagination and sorting"
          isHeaderSticky
          bottomContent={bottomContent}
          bottomContentPlacement="outside"
          classNames={{ wrapper: "max-h-[382px]" }}
          className={classNames.wrapper}
          selectedKeys={selectedKeys}
          selectionMode="multiple"
          sortDescriptor={sortDescriptor}
          topContent={topContent}
          topContentPlacement="outside"
          onSelectionChange={setSelectedKeys}
          onSortChange={setSortDescriptor}
        >
          <TableHeader columns={headerColumns}>
            {(column) => (
              <TableColumn
                key={column.uid}
                align={column.uid === "actions" ? "center" : "start"}
                allowsSorting={column.sortable}
              >
                {column.name}
              </TableColumn>
            )}
          </TableHeader>

          <TableBody emptyContent="No product found" items={sortedItems}>
            {(item) => (
              <TableRow key={item.id}>
                {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    )
  );
}
