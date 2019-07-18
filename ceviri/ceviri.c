#include <Python.h>
#include "lpyhook.h"

extern PyObject* PyObject_GetAttr(PyObject *v, PyObject *name);

PyObject *
translated_PyObject_GetAttr(PyObject *v, PyObject *name)
{
    __asm__("NOP");
    PyTypeObject *tp = Py_TYPE(v);
    printf("%s", PyUnicode_AsUTF8(name));
    if (!PyUnicode_Check(name)) {
        PyErr_Format(PyExc_TypeError,
                     "attribute name must be string, not '%.200s'",
                     name->ob_type->tp_name);
        return NULL;
    }
    if (tp->tp_getattro != NULL)
        return (*tp->tp_getattro)(v, name);
    if (tp->tp_getattr != NULL) {
        const char *name_str = PyUnicode_AsUTF8(name);
        if (name_str == NULL)
            return NULL;
        return (*tp->tp_getattr)(v, (char *)name_str);
    }
    PyErr_Format(PyExc_AttributeError,
                 "'%.50s' object has no attribute '%U'",
                 tp->tp_name, name);
    return NULL;
}

static PyMethodDef module_methods[] = {
    {NULL}
};

static struct PyModuleDef ceviri =
{
    PyModuleDef_HEAD_INIT,
    "ceviri",
    NULL,
    -1, 
    module_methods
};

PyMODINIT_FUNC PyInit_ceviri(void) {
    __asm__("");
    lpyhook(PyObject_GetAttr, &translated_PyObject_GetAttr);
    return PyModule_Create(&ceviri);
}
