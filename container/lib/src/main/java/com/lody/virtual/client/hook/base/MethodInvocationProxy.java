package com.lody.virtual.client.hook.base;

import android.content.Context;

import com.lody.virtual.client.core.InvocationStubManager;
import com.lody.virtual.client.core.VirtualCore;
import com.lody.virtual.client.hook.annotations.Inject;
import com.lody.virtual.client.hook.annotations.LogInvocation;
import com.lody.virtual.client.hook.annotations.SkipInject;
import com.lody.virtual.client.interfaces.IInjector;

import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

/**
 * @author Lody
 * <p>
 * This class is responsible with:
 * - Instantiating a {@link MethodInvocationStub.HookInvocationHandler} on {@link #getInvocationStub()} ()}
 * - Install a bunch of {@link MethodProxy}s, either with a @{@link Inject} annotation or manually
 * calling {@link #addMethodProxy(MethodProxy)} from {@link #onBindMethods()}
 * - Install the hooked object on the Runtime via {@link #inject()}
 * <p>
 * All {@link MethodInvocationProxy}s (plus a couple of other @{@link IInjector}s are installed by
 * {@link InvocationStubManager}
 * @see Inject
 */
public abstract class MethodInvocationProxy<T extends MethodInvocationStub> implements IInjector {

    protected T mInvocationStub;
    static protected Map<Class<?>, List<MethodProxy>> mAdditionalProxies = new HashMap<>();

    /**
     *
     * @param mp the method proxy. When called, the first element in the `args` list will be the next
     *           method proxy in the chain (possibly null)
     */
    public static void addAdditionalProxy(Class<?> cl, MethodProxy mp) {
        List<MethodProxy> l = mAdditionalProxies.get(cl);
        if(l == null) {
            l = new ArrayList<>();
            mAdditionalProxies.put(cl, l);
        }
        l.add(mp);
    }

    private static class FunctionMethodProxy extends MethodProxy {

        private String mName;
        private Method mF;

        FunctionMethodProxy(String name, Method f) {
            super();
            mName = name;
            mF = f;
        }

        @Override
        public String getMethodName() {
            return mName;
        }

        @Override
        public Object call(Object who, Method method, Object... args) throws Throwable {
            return mF.invoke(null, who, method, args);
        }
    }

    /**
     *
     * @param name name of the method proxy
     * @param f static method that will handle the call. It will be invoked with `null` as invokation
     *          object and with `who`, `method` and `args` as arguments. The first element of `args`
     *          will be the next method proxy in the chain (possibly null).
     */
    public static void addAdditionalProxy(Class<?> cl, String name, Method f) {
        MethodProxy mp = new FunctionMethodProxy(name, f);
        addAdditionalProxy(cl, mp);
    }

    public static void clearAdditionalProxies() {
        mAdditionalProxies.clear();
    }

    public MethodInvocationProxy(T invocationStub) {
        this.mInvocationStub = invocationStub;
        onBindMethods();
        afterHookApply(invocationStub);

        LogInvocation loggingAnnotation = getClass().getAnnotation(LogInvocation.class);
        if (loggingAnnotation != null) {
            invocationStub.setInvocationLoggingCondition(loggingAnnotation.value());
        }
    }

    protected void onBindMethods() {

        if (mInvocationStub == null) {
            return;
        }
        Class<? extends MethodInvocationProxy> clazz = getClass();
        Inject inject = clazz.getAnnotation(Inject.class);
        if (inject != null) {
            Class<?> proxiesClass = inject.value();
            Class<?>[] innerClasses = proxiesClass.getDeclaredClasses();
            for (Class<?> innerClass : innerClasses) {
                if (!Modifier.isAbstract(innerClass.getModifiers())
                        && MethodProxy.class.isAssignableFrom(innerClass)
                        && innerClass.getAnnotation(SkipInject.class) == null) {
                    addMethodProxy(innerClass);
                }
            }
            for (Method method : proxiesClass.getMethods()) {
                if (!Modifier.isStatic(method.getModifiers())) {
                    continue;
                }
                if (method.getAnnotation(SkipInject.class) != null) {
                    continue;
                }
                addMethodProxy(new DirectCallMethodProxy(method));
            }
        }
    }

    private static final class DirectCallMethodProxy extends StaticMethodProxy {

        private Method directCallMethod;

        public DirectCallMethodProxy(Method method) {
            super(method.getName());
            this.directCallMethod = method;
        }

        @Override
        public Object call(Object who, Method method, Object... args) throws Throwable {
            return directCallMethod.invoke(null, who, method, args);
        }
    }

    private void addMethodProxy(Class<?> hookType) {
        try {
            Constructor<?> constructor = hookType.getDeclaredConstructors()[0];
            if (!constructor.isAccessible()) {
                constructor.setAccessible(true);
            }
            MethodProxy methodProxy;
            if (constructor.getParameterTypes().length == 0) {
                methodProxy = (MethodProxy) constructor.newInstance();
            } else {
                methodProxy = (MethodProxy) constructor.newInstance(this);
            }
            mInvocationStub.addMethodProxy(methodProxy);
        } catch (Throwable e) {
            throw new RuntimeException("Unable to instance Hook : " + hookType + " : " + e.getMessage());
        }
    }

    public MethodProxy addMethodProxy(MethodProxy methodProxy) {
        return mInvocationStub.addMethodProxy(methodProxy);
    }

    public void setDefaultMethodProxy(MethodProxy methodProxy) {
        mInvocationStub.setDefaultMethodProxy(methodProxy);
    }

    protected void afterHookApply(T delegate) {
        Class<?> cl = getClass();
        List<MethodProxy> l = mAdditionalProxies.get(cl);
        if(l != null) {
            for(MethodProxy p : l) {
                delegate.chainMethodProxy(p);
            }
        }
    }

    @Override
    public abstract void inject() throws Throwable;

    public Context getContext() {
        return VirtualCore.get().getContext();
    }

    public T getInvocationStub() {
        return mInvocationStub;
    }
}
