import { Icons } from "./Icons";
const { Search } = Icons;
export default function Topbar(){
  return (
    <div className="flex items-center justify-between py-4 px-6">
      <h1 className="text-2xl font-semibold">My Cloud</h1>
      <div className="flex items-center gap-3">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 opacity-50"/>
          <input placeholder="Search your file"
            className="pl-9 pr-3 py-2 rounded-xl bg-white shadow-soft outline-none w-72"/>
        </div>
        <div className="w-9 h-9 rounded-full bg-gray-200"/>
      </div>
    </div>
  );
}
