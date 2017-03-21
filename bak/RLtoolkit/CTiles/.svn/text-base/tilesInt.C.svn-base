
#include <Python.h>
#include "tiles.h"

typedef struct {
    PyObject_HEAD
    collision_table* ct;
} CollisionTable;

static void
CollisionTable_dealloc(CollisionTable* self)
{
    if (self->ct != NULL)
        //free(self->ct);
        delete self->ct;
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject * CollisionTable_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CollisionTable *self;
    self = (CollisionTable*) type->tp_alloc(type, 0);
    if (self != NULL)
    {
        self->ct = NULL;//(collision_table*)malloc(sizeof(collision_table));
    }
    
    return (PyObject *) self;
}

static int CollisionTable_init(CollisionTable *self, PyObject *args, PyObject *kwds)
{
    int size;
    int isafety;
    PyObject* safety;
    static char *kwlist[] = {"sizeval", "safetyval", NULL};
    if (! PyArg_ParseTupleAndKeywords(args, kwds, "iO!", kwlist, &size, &PyString_Type,&safety))
        return -1;
    //*(self->ct) = collision_table(size,safety);
    if (strcmp(PyString_AsString(safety),"unsafe") == 0)
	isafety = 0;
    else
	isafety = 1;
    self->ct = new collision_table(size,isafety);
    return 0;
}

static PyObject* CollisionTable_reset(CollisionTable* self)
{
    self->ct->reset();
    return Py_BuildValue("");
}

static PyObject* CollisionTable_usage(CollisionTable* self)
{
    int ret;
    
    ret = self->ct->usage();
    return PyInt_FromLong(ret);
}

static PyObject* CollisionTable_save(CollisionTable* self, PyObject* args)
{
    int file;
    if (!PyArg_ParseTuple(args, "i", &file))
        return NULL;
    self->ct->save(file);
    return Py_BuildValue("");
}

static PyObject* CollisionTable_restore(CollisionTable* self, PyObject* args)
{
    int file;
    if (!PyArg_ParseTuple(args, "i", &file))
        return NULL;
    self->ct->restore(file);
    return Py_BuildValue("");
}

//static PyMemberDef CollisionTable_members[] = {
//    {NULL}  /* Sentinel */
//};

static PyMethodDef CollisionTable_methods[] = {
    {"reset", (PyCFunction)CollisionTable_reset, METH_NOARGS,""},
    {"usage", (PyCFunction)CollisionTable_usage, METH_NOARGS,""},
    {"save", (PyCFunction)CollisionTable_save, METH_NOARGS,""},
    {"restore", (PyCFunction)CollisionTable_restore, METH_NOARGS,""},
    {NULL}  /* Sentinel */
};

static PyTypeObject CollisionTableType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "tiles.CollisionTable",             /*tp_name*/
    sizeof(CollisionTable),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "CollisionTable objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    CollisionTable_methods,             /* tp_methods */
    0,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)CollisionTable_init,      /* tp_init */
    0,                         /* tp_alloc */
    CollisionTable_new,                 /* tp_new */
};

static PyObject * tiles_LoadTiles(PyObject *self, PyObject *args)
{
    PyObject * tiles_list = NULL;
    int* the_tiles = NULL;
    int start_element;
    int num_tilings;
    PyObject* memorctable = NULL;
    collision_table* ct = NULL;
    int memory_size;
    PyObject * variables_list = NULL;
    float* variables = NULL;
    int num_variables;
    PyObject * ints_list = NULL;
    int* ints = NULL;
    int num_ints = 0;
    int i;

    if (!PyArg_ParseTuple(args, "O!iiOO!|O!",&PyList_Type, &tiles_list,
                                                    &start_element,
                                                    &num_tilings,&memorctable,
                                                    &PyList_Type, &variables_list,
                                                    &PyList_Type, &ints_list))
        return NULL;


    variables = (float*)malloc(PyList_Size(variables_list) *sizeof(float));
    the_tiles = (int*)malloc(num_tilings*sizeof(int));

    if (ints_list != NULL && PyList_Size(ints_list) > 0)
    {
        num_ints = PyList_Size(ints_list);
        ints = (int*)malloc(num_ints*sizeof(int));
        for (i = 0; i < num_ints; i++)
            ints[i] = PyInt_AsLong(PyList_GetItem(ints_list,i));
    }
    
    num_variables = PyList_Size(variables_list);

    for (i = 0; i < num_variables; i++)
        variables[i] = PyFloat_AsDouble(PyList_GetItem(variables_list,i));

    if (PyObject_IsInstance(memorctable,(PyObject*)&CollisionTableType))
    {
        ct = ((CollisionTable*)memorctable)->ct;
        tiles(the_tiles,num_tilings,ct,variables,num_variables,ints,num_ints);
    }
    else
    {
        memory_size = PyInt_AsLong(memorctable);
        tiles(the_tiles,num_tilings,memory_size,variables,num_variables,ints,num_ints);
    }

    for (i = num_tilings -1 ; i >= 0; i--)
        PyList_Insert(tiles_list,start_element,PyInt_FromLong(the_tiles[i]));
    return Py_BuildValue("");
}

static PyObject * tiles_GetTiles(PyObject *self, PyObject *args)
{
    PyObject * tiles_list = NULL;
    int* the_tiles;
    int num_tilings;
    PyObject* memorctable = NULL;
    collision_table* ct = NULL;
    int memory_size;
    PyObject * variables_list = NULL;
    float* variables;
    int num_variables;
    PyObject * ints_list = NULL;
    int* ints = NULL;
    int num_ints = 0;
    int i;

    if (!PyArg_ParseTuple(args, "iOO!|O!", &num_tilings,&memorctable,
                                                    &PyList_Type, &variables_list,
                                                    &PyList_Type, &ints_list))
        return NULL;

    variables = (float*)malloc(PyList_Size(variables_list) *sizeof(float));
    the_tiles = (int*)malloc(num_tilings*sizeof(int));
    if (ints_list != NULL && PyList_Size(ints_list) > 0)
    {
        num_ints = PyList_Size(ints_list);
        ints = (int*)malloc(num_ints*sizeof(int));
        for (i = 0; i < num_ints; i++)
            ints[i] = PyInt_AsLong(PyList_GetItem(ints_list,i));
    }
    
    num_variables = PyList_Size(variables_list);

    for (i = 0; i < num_variables; i++)
        variables[i] = PyFloat_AsDouble(PyList_GetItem(variables_list,i));

    if (PyObject_IsInstance(memorctable,(PyObject*)&CollisionTableType))
    {
        ct = ((CollisionTable*)memorctable)->ct;
        tiles(the_tiles,num_tilings,ct,variables,num_variables,ints,num_ints);
    }
    else
    {
        memory_size = PyInt_AsLong(memorctable);
        tiles(the_tiles,num_tilings,memory_size,variables,num_variables,ints,num_ints);
    }
    tiles_list = PyList_New(num_tilings);
    for (i = 0 ; i < num_tilings; i++)
        PyList_SetItem(tiles_list,i,PyInt_FromLong(the_tiles[i]));
    return tiles_list;
}

static PyObject * tiles_LoadTilesWrap(PyObject *self, PyObject *args)
{
    PyObject * tiles_list = NULL;
    int* the_tiles = NULL;
    int start_element;
    int num_tilings;
    PyObject* memorctable = NULL;
    collision_table* ct = NULL;
    int memory_size;
    PyObject * variables_list = NULL;
    float* variables = NULL;
    int num_variables;
    PyObject* wrapwidths_list = NULL;
    int* wrapwidths = NULL;
    PyObject * ints_list = NULL;
    int* ints = NULL;
    int num_ints = 0;
    int i;

    if (!PyArg_ParseTuple(args, "O!iiOO!|O!",&PyList_Type, &tiles_list,
                                                    &start_element,
                                                    &num_tilings,&memorctable,
                                                    &PyList_Type, &variables_list,
                                                    &PyList_Type, &wrapwidths_list,
                                                    &PyList_Type, &ints_list))
        return NULL;

    variables = (float*)malloc(PyList_Size(variables_list) *sizeof(float));
    the_tiles = (int*)malloc(num_tilings*sizeof(int));
    wrapwidths = (int*)malloc(PyList_Size(variables_list)*sizeof(int));

    if (ints_list != NULL && PyList_Size(ints_list) > 0)
    {
        num_ints = PyList_Size(ints_list);
        ints = (int*)malloc(num_ints*sizeof(int));
        for (i = 0; i < num_ints; i++)
            ints[i] = PyInt_AsLong(PyList_GetItem(ints_list,i));
    }
    
    num_variables = PyList_Size(variables_list);

    for (i = 0; i < num_variables; i++)
    {
        variables[i] = PyFloat_AsDouble(PyList_GetItem(variables_list,i));
        wrapwidths[i] = PyInt_AsLong(PyList_GetItem(wrapwidths_list,i));
    }

    if (PyObject_IsInstance(memorctable,(PyObject*)&CollisionTableType))
    {
        ct = ((CollisionTable*)memorctable)->ct;
        tileswrap(the_tiles,num_tilings,ct,variables,num_variables,wrapwidths,ints,num_ints);
    }
    else
    {
        memory_size = PyInt_AsLong(memorctable);
        tileswrap(the_tiles,num_tilings,memory_size,variables,num_variables,wrapwidths,ints,num_ints);
    }

    for (i = num_tilings -1 ; i >= 0; i--)
        PyList_Insert(tiles_list,start_element,PyInt_FromLong(the_tiles[i]));
    return Py_BuildValue("");
}


static PyObject * tiles_GetTilesWrap(PyObject *self, PyObject *args)
{
    PyObject * tiles_list = NULL;
    int* the_tiles = NULL;
    int num_tilings;
    PyObject* memorctable = NULL;
    collision_table* ct = NULL;
    int memory_size;
    PyObject * variables_list = NULL;
    float* variables = NULL;
    int num_variables;
    PyObject * wrapwidths_list = NULL;
    int* wrapwidths = NULL;
    PyObject * ints_list = NULL;
    int* ints = NULL;
    int num_ints = 0;
    int i;

    if (!PyArg_ParseTuple(args, "iOO!O!|O!", &num_tilings,&memorctable,
                                                    &PyList_Type, &variables_list,
                                                    &PyList_Type, &wrapwidths_list,
                                                    &PyList_Type, &ints_list))
        return NULL;

    variables = (float*)malloc(PyList_Size(variables_list) *sizeof(float));
    the_tiles = (int*)malloc(num_tilings*sizeof(int));
    wrapwidths = (int*)malloc(PyList_Size(variables_list) * sizeof(int));
    if (ints_list != NULL && PyList_Size(ints_list) > 0)
    {
        num_ints = PyList_Size(ints_list);
        ints = (int*)malloc(num_ints*sizeof(int));
        for (i = 0; i < num_ints; i++)
            ints[i] = PyInt_AsLong(PyList_GetItem(ints_list,i));
    }
    
    num_variables = PyList_Size(variables_list);

    for (i = 0; i < num_variables; i++)
    {
        variables[i] = PyFloat_AsDouble(PyList_GetItem(variables_list,i));
        wrapwidths[i] = PyInt_AsLong(PyList_GetItem(wrapwidths_list,i));
    }

    if (PyObject_IsInstance(memorctable,(PyObject*)&CollisionTableType))
    {
        ct = ((CollisionTable*)memorctable)->ct;
        tileswrap(the_tiles,num_tilings,ct,variables,num_variables,wrapwidths,ints,num_ints);
    }
    else
    {
        memory_size = PyInt_AsLong(memorctable);
        tileswrap(the_tiles,num_tilings,memory_size,variables,num_variables,wrapwidths,ints,num_ints);
    }
    
    tiles_list = PyList_New(num_tilings);
    for (i = 0 ; i < num_tilings; i++)
        PyList_SetItem(tiles_list,i,PyInt_FromLong(the_tiles[i]));
    return tiles_list;
}


static PyMethodDef TilesMethods[] = {
    {"tiles", tiles_GetTiles, METH_VARARGS,"Get the tiles.."},
    {"loadtiles",tiles_LoadTiles, METH_VARARGS,"Load the tiles..."},
    {"tileswrap", tiles_GetTilesWrap, METH_VARARGS,"Get the tiles..wrap"},
    {"loadtileswrap",tiles_LoadTilesWrap, METH_VARARGS,"Load the tiles...wrap"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC inittiles(void)
{
    PyObject *m;

    if (PyType_Ready(&CollisionTableType) < 0)
        return;
    m = Py_InitModule("tiles", TilesMethods);
    
    if (m == NULL)
        return;
    
    Py_INCREF(&CollisionTableType);
    PyModule_AddObject(m, "CollisionTable", (PyObject *)&CollisionTableType);
}