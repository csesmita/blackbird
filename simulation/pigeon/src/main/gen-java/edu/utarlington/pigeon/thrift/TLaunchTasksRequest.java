/**
 * Autogenerated by Thrift Compiler (0.9.3)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
package edu.utarlington.pigeon.thrift;

import org.apache.thrift.scheme.IScheme;
import org.apache.thrift.scheme.SchemeFactory;
import org.apache.thrift.scheme.StandardScheme;

import org.apache.thrift.scheme.TupleScheme;
import org.apache.thrift.protocol.TTupleProtocol;
import org.apache.thrift.protocol.TProtocolException;
import org.apache.thrift.EncodingUtils;
import org.apache.thrift.TException;
import org.apache.thrift.async.AsyncMethodCallback;
import org.apache.thrift.server.AbstractNonblockingServer.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.EnumMap;
import java.util.Set;
import java.util.HashSet;
import java.util.EnumSet;
import java.util.Collections;
import java.util.BitSet;
import java.nio.ByteBuffer;
import java.util.Arrays;
import javax.annotation.Generated;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SuppressWarnings({"cast", "rawtypes", "serial", "unchecked"})
@Generated(value = "Autogenerated by Thrift Compiler (0.9.3)", date = "2018-11-20")
public class TLaunchTasksRequest implements org.apache.thrift.TBase<TLaunchTasksRequest, TLaunchTasksRequest._Fields>, java.io.Serializable, Cloneable, Comparable<TLaunchTasksRequest> {
  private static final org.apache.thrift.protocol.TStruct STRUCT_DESC = new org.apache.thrift.protocol.TStruct("TLaunchTasksRequest");

  private static final org.apache.thrift.protocol.TField APP_ID_FIELD_DESC = new org.apache.thrift.protocol.TField("appID", org.apache.thrift.protocol.TType.STRING, (short)1);
  private static final org.apache.thrift.protocol.TField USER_FIELD_DESC = new org.apache.thrift.protocol.TField("user", org.apache.thrift.protocol.TType.STRUCT, (short)2);
  private static final org.apache.thrift.protocol.TField REQUEST_ID_FIELD_DESC = new org.apache.thrift.protocol.TField("requestID", org.apache.thrift.protocol.TType.STRING, (short)3);
  private static final org.apache.thrift.protocol.TField SCHEDULER_ADDRESS_FIELD_DESC = new org.apache.thrift.protocol.TField("schedulerAddress", org.apache.thrift.protocol.TType.STRUCT, (short)4);
  private static final org.apache.thrift.protocol.TField TASKS_TO_BE_LAUNCHED_FIELD_DESC = new org.apache.thrift.protocol.TField("tasksToBeLaunched", org.apache.thrift.protocol.TType.LIST, (short)5);

  private static final Map<Class<? extends IScheme>, SchemeFactory> schemes = new HashMap<Class<? extends IScheme>, SchemeFactory>();
  static {
    schemes.put(StandardScheme.class, new TLaunchTasksRequestStandardSchemeFactory());
    schemes.put(TupleScheme.class, new TLaunchTasksRequestTupleSchemeFactory());
  }

  public String appID; // required
  public TUserGroupInfo user; // required
  public String requestID; // required
  public THostPort schedulerAddress; // required
  public List<TTaskLaunchSpec> tasksToBeLaunched; // required

  /** The set of fields this struct contains, along with convenience methods for finding and manipulating them. */
  public enum _Fields implements org.apache.thrift.TFieldIdEnum {
    APP_ID((short)1, "appID"),
    USER((short)2, "user"),
    REQUEST_ID((short)3, "requestID"),
    SCHEDULER_ADDRESS((short)4, "schedulerAddress"),
    TASKS_TO_BE_LAUNCHED((short)5, "tasksToBeLaunched");

    private static final Map<String, _Fields> byName = new HashMap<String, _Fields>();

    static {
      for (_Fields field : EnumSet.allOf(_Fields.class)) {
        byName.put(field.getFieldName(), field);
      }
    }

    /**
     * Find the _Fields constant that matches fieldId, or null if its not found.
     */
    public static _Fields findByThriftId(int fieldId) {
      switch(fieldId) {
        case 1: // APP_ID
          return APP_ID;
        case 2: // USER
          return USER;
        case 3: // REQUEST_ID
          return REQUEST_ID;
        case 4: // SCHEDULER_ADDRESS
          return SCHEDULER_ADDRESS;
        case 5: // TASKS_TO_BE_LAUNCHED
          return TASKS_TO_BE_LAUNCHED;
        default:
          return null;
      }
    }

    /**
     * Find the _Fields constant that matches fieldId, throwing an exception
     * if it is not found.
     */
    public static _Fields findByThriftIdOrThrow(int fieldId) {
      _Fields fields = findByThriftId(fieldId);
      if (fields == null) throw new IllegalArgumentException("Field " + fieldId + " doesn't exist!");
      return fields;
    }

    /**
     * Find the _Fields constant that matches name, or null if its not found.
     */
    public static _Fields findByName(String name) {
      return byName.get(name);
    }

    private final short _thriftId;
    private final String _fieldName;

    _Fields(short thriftId, String fieldName) {
      _thriftId = thriftId;
      _fieldName = fieldName;
    }

    public short getThriftFieldId() {
      return _thriftId;
    }

    public String getFieldName() {
      return _fieldName;
    }
  }

  // isset id assignments
  public static final Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> metaDataMap;
  static {
    Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> tmpMap = new EnumMap<_Fields, org.apache.thrift.meta_data.FieldMetaData>(_Fields.class);
    tmpMap.put(_Fields.APP_ID, new org.apache.thrift.meta_data.FieldMetaData("appID", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING)));
    tmpMap.put(_Fields.USER, new org.apache.thrift.meta_data.FieldMetaData("user", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.StructMetaData(org.apache.thrift.protocol.TType.STRUCT, TUserGroupInfo.class)));
    tmpMap.put(_Fields.REQUEST_ID, new org.apache.thrift.meta_data.FieldMetaData("requestID", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING)));
    tmpMap.put(_Fields.SCHEDULER_ADDRESS, new org.apache.thrift.meta_data.FieldMetaData("schedulerAddress", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.StructMetaData(org.apache.thrift.protocol.TType.STRUCT, THostPort.class)));
    tmpMap.put(_Fields.TASKS_TO_BE_LAUNCHED, new org.apache.thrift.meta_data.FieldMetaData("tasksToBeLaunched", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.ListMetaData(org.apache.thrift.protocol.TType.LIST, 
            new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRUCT            , "TTaskLaunchSpec"))));
    metaDataMap = Collections.unmodifiableMap(tmpMap);
    org.apache.thrift.meta_data.FieldMetaData.addStructMetaDataMap(TLaunchTasksRequest.class, metaDataMap);
  }

  public TLaunchTasksRequest() {
  }

  public TLaunchTasksRequest(
    String appID,
    TUserGroupInfo user,
    String requestID,
    THostPort schedulerAddress,
    List<TTaskLaunchSpec> tasksToBeLaunched)
  {
    this();
    this.appID = appID;
    this.user = user;
    this.requestID = requestID;
    this.schedulerAddress = schedulerAddress;
    this.tasksToBeLaunched = tasksToBeLaunched;
  }

  /**
   * Performs a deep copy on <i>other</i>.
   */
  public TLaunchTasksRequest(TLaunchTasksRequest other) {
    if (other.isSetAppID()) {
      this.appID = other.appID;
    }
    if (other.isSetUser()) {
      this.user = new TUserGroupInfo(other.user);
    }
    if (other.isSetRequestID()) {
      this.requestID = other.requestID;
    }
    if (other.isSetSchedulerAddress()) {
      this.schedulerAddress = new THostPort(other.schedulerAddress);
    }
    if (other.isSetTasksToBeLaunched()) {
      List<TTaskLaunchSpec> __this__tasksToBeLaunched = new ArrayList<TTaskLaunchSpec>(other.tasksToBeLaunched.size());
      for (TTaskLaunchSpec other_element : other.tasksToBeLaunched) {
        __this__tasksToBeLaunched.add(other_element);
      }
      this.tasksToBeLaunched = __this__tasksToBeLaunched;
    }
  }

  public TLaunchTasksRequest deepCopy() {
    return new TLaunchTasksRequest(this);
  }

  @Override
  public void clear() {
    this.appID = null;
    this.user = null;
    this.requestID = null;
    this.schedulerAddress = null;
    this.tasksToBeLaunched = null;
  }

  public String getAppID() {
    return this.appID;
  }

  public TLaunchTasksRequest setAppID(String appID) {
    this.appID = appID;
    return this;
  }

  public void unsetAppID() {
    this.appID = null;
  }

  /** Returns true if field appID is set (has been assigned a value) and false otherwise */
  public boolean isSetAppID() {
    return this.appID != null;
  }

  public void setAppIDIsSet(boolean value) {
    if (!value) {
      this.appID = null;
    }
  }

  public TUserGroupInfo getUser() {
    return this.user;
  }

  public TLaunchTasksRequest setUser(TUserGroupInfo user) {
    this.user = user;
    return this;
  }

  public void unsetUser() {
    this.user = null;
  }

  /** Returns true if field user is set (has been assigned a value) and false otherwise */
  public boolean isSetUser() {
    return this.user != null;
  }

  public void setUserIsSet(boolean value) {
    if (!value) {
      this.user = null;
    }
  }

  public String getRequestID() {
    return this.requestID;
  }

  public TLaunchTasksRequest setRequestID(String requestID) {
    this.requestID = requestID;
    return this;
  }

  public void unsetRequestID() {
    this.requestID = null;
  }

  /** Returns true if field requestID is set (has been assigned a value) and false otherwise */
  public boolean isSetRequestID() {
    return this.requestID != null;
  }

  public void setRequestIDIsSet(boolean value) {
    if (!value) {
      this.requestID = null;
    }
  }

  public THostPort getSchedulerAddress() {
    return this.schedulerAddress;
  }

  public TLaunchTasksRequest setSchedulerAddress(THostPort schedulerAddress) {
    this.schedulerAddress = schedulerAddress;
    return this;
  }

  public void unsetSchedulerAddress() {
    this.schedulerAddress = null;
  }

  /** Returns true if field schedulerAddress is set (has been assigned a value) and false otherwise */
  public boolean isSetSchedulerAddress() {
    return this.schedulerAddress != null;
  }

  public void setSchedulerAddressIsSet(boolean value) {
    if (!value) {
      this.schedulerAddress = null;
    }
  }

  public int getTasksToBeLaunchedSize() {
    return (this.tasksToBeLaunched == null) ? 0 : this.tasksToBeLaunched.size();
  }

  public java.util.Iterator<TTaskLaunchSpec> getTasksToBeLaunchedIterator() {
    return (this.tasksToBeLaunched == null) ? null : this.tasksToBeLaunched.iterator();
  }

  public void addToTasksToBeLaunched(TTaskLaunchSpec elem) {
    if (this.tasksToBeLaunched == null) {
      this.tasksToBeLaunched = new ArrayList<TTaskLaunchSpec>();
    }
    this.tasksToBeLaunched.add(elem);
  }

  public List<TTaskLaunchSpec> getTasksToBeLaunched() {
    return this.tasksToBeLaunched;
  }

  public TLaunchTasksRequest setTasksToBeLaunched(List<TTaskLaunchSpec> tasksToBeLaunched) {
    this.tasksToBeLaunched = tasksToBeLaunched;
    return this;
  }

  public void unsetTasksToBeLaunched() {
    this.tasksToBeLaunched = null;
  }

  /** Returns true if field tasksToBeLaunched is set (has been assigned a value) and false otherwise */
  public boolean isSetTasksToBeLaunched() {
    return this.tasksToBeLaunched != null;
  }

  public void setTasksToBeLaunchedIsSet(boolean value) {
    if (!value) {
      this.tasksToBeLaunched = null;
    }
  }

  public void setFieldValue(_Fields field, Object value) {
    switch (field) {
    case APP_ID:
      if (value == null) {
        unsetAppID();
      } else {
        setAppID((String)value);
      }
      break;

    case USER:
      if (value == null) {
        unsetUser();
      } else {
        setUser((TUserGroupInfo)value);
      }
      break;

    case REQUEST_ID:
      if (value == null) {
        unsetRequestID();
      } else {
        setRequestID((String)value);
      }
      break;

    case SCHEDULER_ADDRESS:
      if (value == null) {
        unsetSchedulerAddress();
      } else {
        setSchedulerAddress((THostPort)value);
      }
      break;

    case TASKS_TO_BE_LAUNCHED:
      if (value == null) {
        unsetTasksToBeLaunched();
      } else {
        setTasksToBeLaunched((List<TTaskLaunchSpec>)value);
      }
      break;

    }
  }

  public Object getFieldValue(_Fields field) {
    switch (field) {
    case APP_ID:
      return getAppID();

    case USER:
      return getUser();

    case REQUEST_ID:
      return getRequestID();

    case SCHEDULER_ADDRESS:
      return getSchedulerAddress();

    case TASKS_TO_BE_LAUNCHED:
      return getTasksToBeLaunched();

    }
    throw new IllegalStateException();
  }

  /** Returns true if field corresponding to fieldID is set (has been assigned a value) and false otherwise */
  public boolean isSet(_Fields field) {
    if (field == null) {
      throw new IllegalArgumentException();
    }

    switch (field) {
    case APP_ID:
      return isSetAppID();
    case USER:
      return isSetUser();
    case REQUEST_ID:
      return isSetRequestID();
    case SCHEDULER_ADDRESS:
      return isSetSchedulerAddress();
    case TASKS_TO_BE_LAUNCHED:
      return isSetTasksToBeLaunched();
    }
    throw new IllegalStateException();
  }

  @Override
  public boolean equals(Object that) {
    if (that == null)
      return false;
    if (that instanceof TLaunchTasksRequest)
      return this.equals((TLaunchTasksRequest)that);
    return false;
  }

  public boolean equals(TLaunchTasksRequest that) {
    if (that == null)
      return false;

    boolean this_present_appID = true && this.isSetAppID();
    boolean that_present_appID = true && that.isSetAppID();
    if (this_present_appID || that_present_appID) {
      if (!(this_present_appID && that_present_appID))
        return false;
      if (!this.appID.equals(that.appID))
        return false;
    }

    boolean this_present_user = true && this.isSetUser();
    boolean that_present_user = true && that.isSetUser();
    if (this_present_user || that_present_user) {
      if (!(this_present_user && that_present_user))
        return false;
      if (!this.user.equals(that.user))
        return false;
    }

    boolean this_present_requestID = true && this.isSetRequestID();
    boolean that_present_requestID = true && that.isSetRequestID();
    if (this_present_requestID || that_present_requestID) {
      if (!(this_present_requestID && that_present_requestID))
        return false;
      if (!this.requestID.equals(that.requestID))
        return false;
    }

    boolean this_present_schedulerAddress = true && this.isSetSchedulerAddress();
    boolean that_present_schedulerAddress = true && that.isSetSchedulerAddress();
    if (this_present_schedulerAddress || that_present_schedulerAddress) {
      if (!(this_present_schedulerAddress && that_present_schedulerAddress))
        return false;
      if (!this.schedulerAddress.equals(that.schedulerAddress))
        return false;
    }

    boolean this_present_tasksToBeLaunched = true && this.isSetTasksToBeLaunched();
    boolean that_present_tasksToBeLaunched = true && that.isSetTasksToBeLaunched();
    if (this_present_tasksToBeLaunched || that_present_tasksToBeLaunched) {
      if (!(this_present_tasksToBeLaunched && that_present_tasksToBeLaunched))
        return false;
      if (!this.tasksToBeLaunched.equals(that.tasksToBeLaunched))
        return false;
    }

    return true;
  }

  @Override
  public int hashCode() {
    List<Object> list = new ArrayList<Object>();

    boolean present_appID = true && (isSetAppID());
    list.add(present_appID);
    if (present_appID)
      list.add(appID);

    boolean present_user = true && (isSetUser());
    list.add(present_user);
    if (present_user)
      list.add(user);

    boolean present_requestID = true && (isSetRequestID());
    list.add(present_requestID);
    if (present_requestID)
      list.add(requestID);

    boolean present_schedulerAddress = true && (isSetSchedulerAddress());
    list.add(present_schedulerAddress);
    if (present_schedulerAddress)
      list.add(schedulerAddress);

    boolean present_tasksToBeLaunched = true && (isSetTasksToBeLaunched());
    list.add(present_tasksToBeLaunched);
    if (present_tasksToBeLaunched)
      list.add(tasksToBeLaunched);

    return list.hashCode();
  }

  @Override
  public int compareTo(TLaunchTasksRequest other) {
    if (!getClass().equals(other.getClass())) {
      return getClass().getName().compareTo(other.getClass().getName());
    }

    int lastComparison = 0;

    lastComparison = Boolean.valueOf(isSetAppID()).compareTo(other.isSetAppID());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetAppID()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.appID, other.appID);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = Boolean.valueOf(isSetUser()).compareTo(other.isSetUser());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetUser()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.user, other.user);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = Boolean.valueOf(isSetRequestID()).compareTo(other.isSetRequestID());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetRequestID()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.requestID, other.requestID);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = Boolean.valueOf(isSetSchedulerAddress()).compareTo(other.isSetSchedulerAddress());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetSchedulerAddress()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.schedulerAddress, other.schedulerAddress);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = Boolean.valueOf(isSetTasksToBeLaunched()).compareTo(other.isSetTasksToBeLaunched());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetTasksToBeLaunched()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.tasksToBeLaunched, other.tasksToBeLaunched);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    return 0;
  }

  public _Fields fieldForId(int fieldId) {
    return _Fields.findByThriftId(fieldId);
  }

  public void read(org.apache.thrift.protocol.TProtocol iprot) throws org.apache.thrift.TException {
    schemes.get(iprot.getScheme()).getScheme().read(iprot, this);
  }

  public void write(org.apache.thrift.protocol.TProtocol oprot) throws org.apache.thrift.TException {
    schemes.get(oprot.getScheme()).getScheme().write(oprot, this);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder("TLaunchTasksRequest(");
    boolean first = true;

    sb.append("appID:");
    if (this.appID == null) {
      sb.append("null");
    } else {
      sb.append(this.appID);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("user:");
    if (this.user == null) {
      sb.append("null");
    } else {
      sb.append(this.user);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("requestID:");
    if (this.requestID == null) {
      sb.append("null");
    } else {
      sb.append(this.requestID);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("schedulerAddress:");
    if (this.schedulerAddress == null) {
      sb.append("null");
    } else {
      sb.append(this.schedulerAddress);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("tasksToBeLaunched:");
    if (this.tasksToBeLaunched == null) {
      sb.append("null");
    } else {
      sb.append(this.tasksToBeLaunched);
    }
    first = false;
    sb.append(")");
    return sb.toString();
  }

  public void validate() throws org.apache.thrift.TException {
    // check for required fields
    // check for sub-struct validity
    if (user != null) {
      user.validate();
    }
    if (schedulerAddress != null) {
      schedulerAddress.validate();
    }
  }

  private void writeObject(java.io.ObjectOutputStream out) throws java.io.IOException {
    try {
      write(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(out)));
    } catch (org.apache.thrift.TException te) {
      throw new java.io.IOException(te);
    }
  }

  private void readObject(java.io.ObjectInputStream in) throws java.io.IOException, ClassNotFoundException {
    try {
      read(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(in)));
    } catch (org.apache.thrift.TException te) {
      throw new java.io.IOException(te);
    }
  }

  private static class TLaunchTasksRequestStandardSchemeFactory implements SchemeFactory {
    public TLaunchTasksRequestStandardScheme getScheme() {
      return new TLaunchTasksRequestStandardScheme();
    }
  }

  private static class TLaunchTasksRequestStandardScheme extends StandardScheme<TLaunchTasksRequest> {

    public void read(org.apache.thrift.protocol.TProtocol iprot, TLaunchTasksRequest struct) throws org.apache.thrift.TException {
      org.apache.thrift.protocol.TField schemeField;
      iprot.readStructBegin();
      while (true)
      {
        schemeField = iprot.readFieldBegin();
        if (schemeField.type == org.apache.thrift.protocol.TType.STOP) { 
          break;
        }
        switch (schemeField.id) {
          case 1: // APP_ID
            if (schemeField.type == org.apache.thrift.protocol.TType.STRING) {
              struct.appID = iprot.readString();
              struct.setAppIDIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 2: // USER
            if (schemeField.type == org.apache.thrift.protocol.TType.STRUCT) {
              struct.user = new TUserGroupInfo();
              struct.user.read(iprot);
              struct.setUserIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 3: // REQUEST_ID
            if (schemeField.type == org.apache.thrift.protocol.TType.STRING) {
              struct.requestID = iprot.readString();
              struct.setRequestIDIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 4: // SCHEDULER_ADDRESS
            if (schemeField.type == org.apache.thrift.protocol.TType.STRUCT) {
              struct.schedulerAddress = new THostPort();
              struct.schedulerAddress.read(iprot);
              struct.setSchedulerAddressIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 5: // TASKS_TO_BE_LAUNCHED
            if (schemeField.type == org.apache.thrift.protocol.TType.LIST) {
              {
                org.apache.thrift.protocol.TList _list24 = iprot.readListBegin();
                struct.tasksToBeLaunched = new ArrayList<TTaskLaunchSpec>(_list24.size);
                TTaskLaunchSpec _elem25;
                for (int _i26 = 0; _i26 < _list24.size; ++_i26)
                {
                  _elem25 = new TTaskLaunchSpec();
                  _elem25.read(iprot);
                  struct.tasksToBeLaunched.add(_elem25);
                }
                iprot.readListEnd();
              }
              struct.setTasksToBeLaunchedIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          default:
            org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
        }
        iprot.readFieldEnd();
      }
      iprot.readStructEnd();

      // check for required fields of primitive type, which can't be checked in the validate method
      struct.validate();
    }

    public void write(org.apache.thrift.protocol.TProtocol oprot, TLaunchTasksRequest struct) throws org.apache.thrift.TException {
      struct.validate();

      oprot.writeStructBegin(STRUCT_DESC);
      if (struct.appID != null) {
        oprot.writeFieldBegin(APP_ID_FIELD_DESC);
        oprot.writeString(struct.appID);
        oprot.writeFieldEnd();
      }
      if (struct.user != null) {
        oprot.writeFieldBegin(USER_FIELD_DESC);
        struct.user.write(oprot);
        oprot.writeFieldEnd();
      }
      if (struct.requestID != null) {
        oprot.writeFieldBegin(REQUEST_ID_FIELD_DESC);
        oprot.writeString(struct.requestID);
        oprot.writeFieldEnd();
      }
      if (struct.schedulerAddress != null) {
        oprot.writeFieldBegin(SCHEDULER_ADDRESS_FIELD_DESC);
        struct.schedulerAddress.write(oprot);
        oprot.writeFieldEnd();
      }
      if (struct.tasksToBeLaunched != null) {
        oprot.writeFieldBegin(TASKS_TO_BE_LAUNCHED_FIELD_DESC);
        {
          oprot.writeListBegin(new org.apache.thrift.protocol.TList(org.apache.thrift.protocol.TType.STRUCT, struct.tasksToBeLaunched.size()));
          for (TTaskLaunchSpec _iter27 : struct.tasksToBeLaunched)
          {
            _iter27.write(oprot);
          }
          oprot.writeListEnd();
        }
        oprot.writeFieldEnd();
      }
      oprot.writeFieldStop();
      oprot.writeStructEnd();
    }

  }

  private static class TLaunchTasksRequestTupleSchemeFactory implements SchemeFactory {
    public TLaunchTasksRequestTupleScheme getScheme() {
      return new TLaunchTasksRequestTupleScheme();
    }
  }

  private static class TLaunchTasksRequestTupleScheme extends TupleScheme<TLaunchTasksRequest> {

    @Override
    public void write(org.apache.thrift.protocol.TProtocol prot, TLaunchTasksRequest struct) throws org.apache.thrift.TException {
      TTupleProtocol oprot = (TTupleProtocol) prot;
      BitSet optionals = new BitSet();
      if (struct.isSetAppID()) {
        optionals.set(0);
      }
      if (struct.isSetUser()) {
        optionals.set(1);
      }
      if (struct.isSetRequestID()) {
        optionals.set(2);
      }
      if (struct.isSetSchedulerAddress()) {
        optionals.set(3);
      }
      if (struct.isSetTasksToBeLaunched()) {
        optionals.set(4);
      }
      oprot.writeBitSet(optionals, 5);
      if (struct.isSetAppID()) {
        oprot.writeString(struct.appID);
      }
      if (struct.isSetUser()) {
        struct.user.write(oprot);
      }
      if (struct.isSetRequestID()) {
        oprot.writeString(struct.requestID);
      }
      if (struct.isSetSchedulerAddress()) {
        struct.schedulerAddress.write(oprot);
      }
      if (struct.isSetTasksToBeLaunched()) {
        {
          oprot.writeI32(struct.tasksToBeLaunched.size());
          for (TTaskLaunchSpec _iter28 : struct.tasksToBeLaunched)
          {
            _iter28.write(oprot);
          }
        }
      }
    }

    @Override
    public void read(org.apache.thrift.protocol.TProtocol prot, TLaunchTasksRequest struct) throws org.apache.thrift.TException {
      TTupleProtocol iprot = (TTupleProtocol) prot;
      BitSet incoming = iprot.readBitSet(5);
      if (incoming.get(0)) {
        struct.appID = iprot.readString();
        struct.setAppIDIsSet(true);
      }
      if (incoming.get(1)) {
        struct.user = new TUserGroupInfo();
        struct.user.read(iprot);
        struct.setUserIsSet(true);
      }
      if (incoming.get(2)) {
        struct.requestID = iprot.readString();
        struct.setRequestIDIsSet(true);
      }
      if (incoming.get(3)) {
        struct.schedulerAddress = new THostPort();
        struct.schedulerAddress.read(iprot);
        struct.setSchedulerAddressIsSet(true);
      }
      if (incoming.get(4)) {
        {
          org.apache.thrift.protocol.TList _list29 = new org.apache.thrift.protocol.TList(org.apache.thrift.protocol.TType.STRUCT, iprot.readI32());
          struct.tasksToBeLaunched = new ArrayList<TTaskLaunchSpec>(_list29.size);
          TTaskLaunchSpec _elem30;
          for (int _i31 = 0; _i31 < _list29.size; ++_i31)
          {
            _elem30 = new TTaskLaunchSpec();
            _elem30.read(iprot);
            struct.tasksToBeLaunched.add(_elem30);
          }
        }
        struct.setTasksToBeLaunchedIsSet(true);
      }
    }
  }

}

