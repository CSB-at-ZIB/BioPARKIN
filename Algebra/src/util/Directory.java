/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package util;
import java.io.File;
import java.io.FileFilter;

import java.util.HashSet;
import java.util.Iterator;
/**
 * A class providing methods to deal with directories and
 * their subdirectories. <b>Note</b>, that the subdirectories
 * only get listed after calling {@link Directory#hasChildren() }
 * @author hendrik1
 */
public class Directory implements Iterable<Directory>, Comparable<Directory> {
    /**an error string indicating the children objects haven't
     * been listed*/
    private static final String ERROR_STR1 = "\nIterator method called before calling hasChildren!";
    /**an error string indicating that compareTo was called on at least one
       null directory*/
    private static final String ERROR_STR2 = "\nNull directory - not comparable!";
    /**a string indicating: no such directory*/
    private static final String NULL_STR1 = "null directory - no such directory";
    /**the directory object*/
    private File dir;
    /**a set of all children directories*/
    private HashSet<Directory> children;
    /**a flag indicating whether or not the children have been listed*/
    private boolean childFlag;
    /**
     * Constructs an empty directory
     */
    private Directory (){
        children = new HashSet<Directory> ();
    }
    /**
     * Constructs a directory where <tt>dir</tt> specifies the
     * absolute path
     * @param dir the absolute path
     */
    public Directory (String dir){
        this();
        setDirectory(new File (dir));
    }
    /**
     * Constructs a directory where <tt>dir</tt> specifies the
     * directory
     * @param dir the directory
     */
    public Directory (File dir){
        this();
        setDirectory(dir);
    }
    /**
     * Compares this and <tt>another</tt> directory object
     * lexicographically and returns an integer value negative,
     * zero or positive if this is less, equal or greater than
     * <tt>another</tt>, respectively.
     * @param another another directory
     * @return an integer
     * @throws java.lang.RuntimeException at least one directory does not exist
     */
    public int compareTo (Directory another) throws RuntimeException {
        if(dir==null||another.dir==null)
            throw new RuntimeException (ERROR_STR2);
        return dir.compareTo(another.dir);
    }
    public boolean equals (Object o){
        if(!(o instanceof Directory))
            throw new ClassCastException ("");
        return dir.equals(((Directory) o).dir);
    }
    protected HashSet<Directory> getChildren (){
        return new HashSet<Directory> (children);
    }
    /**
     * Returns true, iff this directory contains
     * subdirectories. <b>Note</b>, that this method has
     * to be called, to initialise the children instance.
     * @return true, if this contains subdirectories
     */
    public boolean hasChildren (){
        if(children.size()==0&&!childFlag){
            childFlag = true;
            File[] list = dir.listFiles();
            if(list.length==0) return false;
            for (int i = 0; i < list.length; i++){
                Directory dirs = new Directory ();
                dirs.setDirectory(list[i]);
                if(dirs.dir!=null) children.add(dirs);
            }            
            return children.size()==0?false:true;
        }
        childFlag = true;
        if(children.size()>0) return true;
        return false;
    }
    public int hashCode (){return dir.hashCode();}
    /**
     * Returns an iterator over all subdirectories of this
     * directory. <b>Note</b>, that calling this method before
     * calling {@link Directory#hasChildren() } will raise an
     * <code>RuntimeException</code>.
     * <p>Example: <li><tt>Directory d = new ...</tt></li>
     * <li><tt>if(d.hashChildren())</tt></li>
     * <li><tt>  Iterator it = d.iterator ()</tt>,</li></p>
     * 
     * such that no exception will be thrown.
     * @return an iterator
     * @throws java.lang.RuntimeException indicates that the subdirectories
     * haven't been listed, yet
     */
    public Iterator<Directory> iterator () throws RuntimeException {
        if(!childFlag) throw new RuntimeException (ERROR_STR1);
        return children.iterator();
    }
    /**
     * Returns a list of all files contained in this
     * directory
     * @return a list of files
     */
    public File[] listFiles (){
        return dir.listFiles();
    }
    /**
     * Returns a list of files matching the provided
     * filter
     * @param filter a filter
     * @return a list of files
     */
    public File[] listFiles (FileFilter filter){
        return dir.listFiles(filter);
    }
    
    private void setDirectory (File dir){
        if(dir.isDirectory()) this.dir = dir;
    }
    /**
     * Returns the absolute path of this directory
     * @return the absolute path
     */
    @Override
    public String toString (){
        if(dir==null) return NULL_STR1;
        return dir.toString();
    }
    public static void main (String[] args) {
        Directory d = new Directory ("C:/Dokumente und Einstellungen/hendrik1/" +
                "Eigene Dateien/Uni Kram/");
        if(d.hasChildren()){
            for (Directory di : d)
                System.out.println(di);
        }
        if(d.hasChildren());
    }
}
