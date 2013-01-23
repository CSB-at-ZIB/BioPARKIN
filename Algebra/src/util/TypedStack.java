/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package util;
import java.util.*;
/**
 * Utility class to wrap arrays of objects of the same
 * type in just one object. <b>Note</b>, that any instance
 * of this class is nested, i.e. the first entry (last) is
 * the outermost instance the next (previous) is the second
 * outermost, and so on. Additionally, this class can
 * construct ascending or descending stacks, depending on the
 * constructor used. For simplicity, this class implements
 * the <code>java.lang.Iterable</code> interface, so the following
 * is permitted:
 * <p><tt>TypedStack stack = ...</tt></p>
 * <p><tt>for (T t : stack){...</tt></p>
 * @author hendrik1
 * @param <T> the type of the array elements to wrap
 */
public class TypedStack<T> implements Iterable<T> {
    /**the current element*/
    private T curr;
    /**the next stack element*/
    protected TypedStack<T> next;
    /**the level of nested stack*/
    private int steep;
    /**flag indicating, whether or not an 
     * iterator has been attached to an instance
     * of this class*/
    protected boolean hasIterator;
    /**the index*/
    private int index;
    /**
     * Constructs an empty stack object of fixed type.
     */
    protected TypedStack (){}
    /**
     * Constructs a descending <code>TypedStack</code> by recursively
     * running "down" the array <tt>stack</tt> starting at <tt>pos</tt>.
     * <b>Note</b>, that <tt>pos>=0&&stack.length-1>=pos</tt> must return
     * true, otherwise an <code>IllegalArgumentException</code> is thrown.
     * @param stack the array
     * @param pos the starting position,
     */
    public TypedStack (T[] stack, int pos){
        steep = stack.length;
        sanityCheck(pos,stack);
        setStackDescending (pos,stack);
    }
    /**
     * Constructs a ascending <code>TypedStack</code> by recursively
     * running "up" the array <tt>stack</tt> starting at <tt>pos</tt>.
     * <b>Note</b>, that <tt>pos>=0&&stack.length-1>=pos</tt> must return
     * true, otherwise an <code>IllegalArgumentException</code> is thrown.
     * @param pos the starting position,
     * @param stack the array
     */
    public TypedStack (int pos, T[] stack){
        steep = stack.length;
        sanityCheck(pos,stack);
        setStackAscending(pos,stack);
    }
    /**
     * Constructs an instance of this class by
     * using the provided iterator <tt>it</tt>
     * running through a collection.
     * @param it an iterator
     */
    public TypedStack (Iterator<T> it){
        if(it.hasNext()){
            curr = it.next();
            if(it.hasNext()){
                steep = 1;
                next = new TypedStack<T> (it,steep);
                next.index = index+1;
            }
        }
    }
    /**
     * Auxiliary constructor: keeps track of the
     * level of nested stack.
     * @param it the iterator
     * @param steep the nestedness count
     */
    private TypedStack (Iterator<T> it, int steep){
        if(it.hasNext()){
            curr = it.next();
            if(it.hasNext()){
                this.steep = steep+1;
                next = new TypedStack<T> (it,this.steep);
                next.index = index+1;
            }
        }
    }
    /**
     * Constructs a new instance of this class by performing
     * a deep copy of <tt>stack</tt>.
     * @param stack the original stack
     */
    public TypedStack (TypedStack<T> stack){
        this(stack.iterator());
    }
    /**
     * Adds all elements provided by the <code>java.util.Iterator</code>
     * <tt>it</tt>, recursively. <b>Note</b>, that null entries are never
     * added. Additionally, an iterator over this stack will prevent any modifications
     * outside the iterator. Thus calling this method while the
     * iterator's <tt>hasNext()</tt> has not returned true, yet will
     * raise an exception.
     * @param it an iterator over an iterable collection
     * @throws java.util.ConcurrentModificationException an iterator is still
     * attached to this object
     */
    public void add (Iterator<T> it) throws ConcurrentModificationException {
        if(it.hasNext()){
            add(it.next());
            if(it.hasNext()) add(it);
        }
        setIndex();
    }
    /**
     * Auxiliary method: runs through the stack and
     * places <tt>element</tt> at the first null element. <b>Note</b>, that
     * an iterator over this stack will prevent any modifications
     * outside the iterator. Thus calling this method while the
     * iterator's <tt>hasNext()</tt> has not returned true, yet will
     * raise an exception.
     * @param element a stack element
     * @throws java.util.ConcurrentModificationException an iterator is still
     * attached to this object
     */
    protected void add (T element) throws ConcurrentModificationException {
        if(hasIterator) throw new ConcurrentModificationException ("\nAn iterator" +
                " is still attached to this object!");
        if(element==null) return;
        if(curr!=null){
            if(next==null)
                next = new TypedStack<T>();
            next.add(element);
            setIndex();
        }
        else{
            curr = element;
        }
    }
    /**
     * Adds the argument <tt>array</tt> to this <code>TypedStack</code>
     * object. <b>Note</b>, that null objects are never added. Additionally,
     * an iterator over this stack will prevent any modifications
     * outside the iterator. Thus calling this method while the
     * iterator's <tt>hasNext()</tt> method has not returned true, yet will
     * raise an exception.
     * @param array an array of objects
     * @throws java.util.ConcurrentModificationException an iterator is still
     * attached to this object
     */
    public void add (T[] array) throws ConcurrentModificationException {
        int length = array.length;
        for (int i = 0; i < length; i++)
                add(array[i]);
    }
    
    /**
     * Adds the <tt>stack</tt> to this object. <b>Note</b>, that
     * an iterator over this stack will prevent any modifications
     * outside the iterator. Thus calling this method while the
     * iterator's <tt>hasNext()</tt> method has not returned true, yet will
     * raise an exception.
     * @param stack another stack
     * @throws java.util.ConcurrentModificationException an iterator is still
     * attached to this object
     */
    public void add (TypedStack<T> stack) throws ConcurrentModificationException {
        add(stack.iterator());
    }
    /**
     * Returns true if and only if this stack object
     * contains at least one stack element <tt>e</tt>,
     * such that <tt>element.equals (e)</tt> returns true.
     * <b>Note</b>, that an iterator over this stack will prevent any modifications
     * outside the iterator. Thus calling this method while the
     * iterator's <tt>hasNext()</tt> has not returned true, yet will
     * raise an exception.
     * @param element an element to look up
     * @return true, if <tt>element</tt> is in the stack
     */
    public boolean contains (T element) throws ConcurrentModificationException {
        if(hasIterator) throw new ConcurrentModificationException ("");
        boolean isin = curr.equals(element);
        return isin?true:next==null?false:next.contains(element);
    }
    /**
     * Returns true if and only if both stacks
     * nested elements return pairwise true on any
     * call to <tt>equals(Object)</tt> and both
     * stacks have the same nested level. <b>Note</b>,
     * this method throws an <code>ClassCastException</code>
     * if <tt>o</tt> is not of type <code>TypedStack</code>
     * @param o another stack
     * @return true if both are pairwise equal
     */
    @Override
    public boolean equals (Object o){
        if(o instanceof TypedStack){
            TypedStack<T> cp = (TypedStack<T>) o;
            if(curr.equals(cp.curr)){
                if(((next==null||cp.next==null)&&
                        !(next==null&&cp.next==null)))
                    return false;
                if(next==null&&cp.next==null) return true;
                else next.equals (cp.next);
                return true;
            } else return false;
        } else throw new ClassCastException ("Found "+o.getClass().getName()+
                "\nRequired: TypedStack");
    }
    /**
     * Returns the current element of this stack
     * @return the current element
     */
    public T getElement (){
        return curr;
    }
    /**
     * Returns the index
     * @return the index
     */
    public int getIndex (){
        return index;
    }
    /**
     * Returns a collection view of all indices of
     * this typed stack
     * @return a collection of all indices
     */
    public HashSet<Integer> getIndexSet (){
        HashSet<Integer> iSet = new HashSet<Integer> ();
        iSet.add(index);
        if(next==null) return iSet;
        iSet.addAll(next.getIndexSet());
        return iSet;
    }
    /**
     * Returns the next substack of this object.
     * @return the next substack
     */
    protected TypedStack<T> getNext(){
        return next;
    }
    /**
     * Returns this stack as a <code>java.util.HashSet</code>
     * @return a collection view of this object
     */
    public HashSet<T> getSet (){
        HashSet<T> set = new HashSet<T> ();
        for (T t : this)
            set.add(t);
        return set;
    }
    public int getSteep (){
        return steep;
    }
    /**
     * Returns a hash code for this object.
     * The hash code is just the sum of all return
     * values of calls to the <tt>hashCode()</tt>
     * method of all nested elements.
     * @return the hash code
     */
    @Override
    public int hashCode (){
        int hash = curr.hashCode();
        if(next!=null)
            hash+= next.hashCode();
        return hash;
    }
    /**
     * Returns an iterator over this stack object.
     * The direction of the iteration strongly depends
     * on the way this object was created (ascending/descending).
     * @return an iterator
     */
    public Iterator<T> iterator (){
        return new TypedIterator (this);
    }
    /**
     * Removes <tt>element</tt> from this stack and
     * returns true, if removal was successful. <b>Note</b>, that
     * an iterator over this stack will prevent any modifications
     * outside the iterator. Thus calling this method while the
     * iterator's <tt>hasNext()</tt> has not returned true, yet will
     * raise an exception.
     * @param element an element to look up
     * @return true, if removed
     * @throws java.util.ConcurrentModificationException an iterator
     * is still attached to this object
     */
    public boolean remove (T element) throws ConcurrentModificationException {
        if(hasIterator) throw new ConcurrentModificationException ("\nAn iterator" +
                " is still attached to this object!");
        if(curr.equals(element)){
            if(next!=null){
                curr = next.curr;
                if(next.next!=null){
                    next = next.next;
                } else next = null;
            } else curr = null;
            setIndex();
            return true;
        } else {
            if(next!=null){
                return next.remove(element);
            }
            return false;
        }
    }
    /**
     * Checks whether the position argument <tt>pos</tt> is
     * in range of the dimension of <tt>stack</tt> - throws
     * an exception if not.
     * @param pos the position argument
     * @param stack the stack
     */
    private void sanityCheck (int pos, T[] stack){
        if(pos<0||pos>=stack.length){
            if(pos<0) throw new IllegalArgumentException ("Negative index: "+pos);
            else throw new IllegalArgumentException ("Exceeding stack dimensions!");
        }
    }
    /**
     * Auxiliary setter: used in the ascending instance constructor
     * @param pos the position
     * @param stack the array
     */
    private void setStackAscending (int pos, T[] stack){
        int length = stack.length;
        if(pos<=length-1&&stack[pos]!=null){
            index = pos;
            curr = stack[pos];
            if(pos<length-1){
                pos++;
                next = new TypedStack<T> (pos,stack);
            }
        }
    }
    /**
     * Auxiliary setter: used in the descending instance constructor
     * @param pos the position
     * @param stack the array
     */
    private void setStackDescending (int pos, T[] stack){
        if(pos>=0&&stack[pos]!=null){
            curr = stack[pos];
            index = stack.length-1-pos;
            if(pos>0){
                pos--;
                next = new TypedStack<T> (stack,pos);
            }
        }
    }

    /**
     * Returns the substack <tt>s</tt> of <tt>this</tt>, starting
     * at <tt>beg</tt>. <b>Note</b>, that this method returns null, if
     * <ol><li><tt>beg</tt> is negative</li>
     * <li><tt>beg</tt> greater than innermost nested level</li></ol>
     * @param beg the begin
     * @return a substack or null
     */
    public TypedStack<T> subStack (int beg){
        if(beg<0) return null;
        Iterator<T> it = iterator();
        int count = 0;
        TypedStack<T> sub = new TypedStack<T> ();
        while (it.hasNext()){
            if(count==beg){
                sub.add(it);
                break;
            } else {
                count++;
                it.next();
            }
        }
        return sub;
    }
    /**
     * Returns a substack <tt>s</tt> of <tt>this</tt>, if
     * and only if <tt>element</tt> is present, otherwise the
     * empty stack is returned. The stack starts at <tt>element</tt>
     * and runs through until the end.
     * @param element the starting element
     * @return a substack starting at element or empty stack
     */
    public TypedStack<T> subStackFrom (T element){
        TypedStack<T> sub = new TypedStack<T> ();
        if(curr.equals(element)){
            sub.add(iterator());
        } else {
            if(next!=null)
                sub.add(next.subStackFrom(element));
        }
        return sub;
    }
    /**
     * Returns a substack <tt>s</tt> of <tt>this</tt>
     * where <tt>element</tt> is the last entry. <b>Note</b>, if
     * <tt>element</tt> is not contained in this stack, a deep
     * copy of <tt>this</tt> is returned.
     * @param element the last element
     * @return a substack ending at <tt>element</tt>
     */
    public TypedStack<T> subStackUntil (T element){
        TypedStack<T> sub = new TypedStack();
        if(!curr.equals(element)){
            sub.add(curr);
            if(next!=null) sub.add(next.subStackUntil(element));
            return sub;
        } else {
            sub.add(curr);
            return sub;
        }
    }
    /**
     * Returns a string representation of this stack object
     * @return a string representing this
     */
    @Override
    public String toString (){
        StringBuilder sb = new StringBuilder ("[");
        Iterator<T> it = iterator();
        while (it.hasNext()){
            T t = it.next();
            if(it.hasNext()) sb.append(t+",");
            else sb.append(t);
        }
        sb.append("]");
        return sb.toString();
    }
    protected void setCurrent (T curr){this.curr = curr;}
    private void setIndex (){
        if(next==null) return;
        if(next.index-index==1){
            next.setIndex();
            return;
        }
        next.index = index+1;
        next.setIndex();
    }
    /*------------------inner class--------------------*/
    /**
     * Auxiliary class: provides functionality of the
     * <code>java.lang.Iterator</code> interface.
     */
    class TypedIterator implements Iterator<T> {
        /**a shallow copy of the current stack*/
        TypedStack<T> loc;
        /**a flag indicating whether <tt>next()</tt> has
         * been called*/
        boolean nextFlag;
        /**
         * Constructs an iterator by referencing the outer
         * class object to the inner field <tt>loc</tt> and
         * run the line of the nested object until null is reached.
         * @param loc the local copy reference
         */
        TypedIterator (TypedStack<T> loc){
            hasIterator = true;
            this.loc = loc;
        }
        public boolean hasNext (){
            if(loc!=null&&loc.curr!=null) return true;
            else {
                hasIterator = false;
                return false;
            }
        }
        public T next (){
            if(hasNext()){
                TypedStack<T> cp = loc;
                loc = loc.next;
                nextFlag = true;
                return cp.curr;
            } return null;
        }
        public void remove (){
            //if(!nextFlag) throw new Un
            if(loc==null){
                curr = null;
                nextFlag = false;
                return;
            }
            TypedStack<T> cp = loc;
            curr = cp.curr;
            next = cp.next;
            setIndex();
        }

    }

    public static void main (String [] args){
        String[] sAr = new String[]{"alpha","beta","gamma","delta"};
        TypedStack<String> sStack = new TypedStack (0,sAr);
        TypedStack<String> sStack1 = new TypedStack (sAr,3);
        System.out.println("full stack = "+sStack);
        System.out.println("\n"+sStack.getIndexSet());
        System.out.println("\n"+sStack1.getIndexSet());
        Random rand = new Random ();
        for (int i = 0; i < 1; i++){
            int val = (int) Math.max(rand.nextInt(4),1);
            TypedStack<String> first = sStack.subStack(1);
            TypedStack<String> second= sStack1.subStack(1);
            System.out.println("substack length: "+val+"\tsubstack: "+first+"\tsteep: "+first.getSteep());
            System.out.println("\n"+first.getIndexSet());
            System.out.println("substack1 length: "+3+"\tsubstack1: "+second+
                    "\tsteep: "+second.getSteep());
            System.out.println("\n"+second.getIndexSet());
            Iterator<String> it1 = first.iterator();
            while(it1.hasNext()){
                String s1 = it1.next();
                it1.remove();
                System.out.println("Removed: "+s1+"\trest: "+first);
                System.out.println("\n"+first.getIndexSet());
            }
            Iterator<String> it2 = second.iterator();
            while(it2.hasNext()){
                String s = it2.next();
                it2.remove();
                System.out.println("Removed: "+s+"\trest: "+second);
                System.out.println("\n"+second.getIndexSet());
            }
            it2 = sStack.iterator();
            second.add(it2);
            System.out.println("Added first stack: "+second+"\ttest equals():"+second.equals(second));
            System.out.println("removal of 'gamma' successeded: "+second.subStackFrom("gamma")+"\t:"+second);
            System.out.println("removal of 'gamma' successeded: "+second.subStackUntil("gamma")+"\t:"+second);
        }
        System.gc();
    }
}
