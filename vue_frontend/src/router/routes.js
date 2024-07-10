const routes = [
  {
    path: "/",
    component: () => import("layouts/SignInLayout.vue"),
    children: [
      {
        path: "",
        name: "login",
        component: () => import("pages/Sections/SignIn/Index.vue"),
      },
    ],
  },
  {
    path: "/dashboard",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "index",
        component: () => import("pages/IndexPage.vue"),
        redirect: { name: "events" },
      },
      {
        path: "eventos",
        name: "events",
        component: () => import("pages/Sections/Events/Index.vue"),
      },
      {
        path: "camaras",
        name: "cameras",
        component: () => import("pages/Sections/Cameras/Index.vue"),
      },
      {
        path: "configuracion",
        name: "settings",
        component: () => import("pages/Sections/Settings/Index.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
