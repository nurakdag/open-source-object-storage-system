import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function Layout(){
  return (
    <div className="bg-slate-100 min-h-dvh text-slate-800">
      <div className="flex max-w-[1400px] mx-auto">
        <Sidebar/>
        <main className="flex-1">
          <Topbar/>
          <div className="px-6 pb-10"><Outlet/></div>
        </main>
      </div>
    </div>
  );
}
