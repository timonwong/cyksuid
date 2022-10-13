#pragma once

#include <array>
#include <chrono>
#include <cstdlib>
#include <cstring>
#include <stdexcept>

constexpr size_t _BYTE_SIZE = 20;
constexpr int64_t KSUID_EPOCH = 1400000000; // in seconds

struct MemoryView {
  const uint8_t* data;
  size_t size;
};

#if _MSC_VER >= 1100 && !defined(_DEBUG)
#define _KL_NOVTABLE __declspec(novtable)
#else
#define _KL_NOVTABLE
#endif

/**
 * Common KSUID interface.
 */
struct _KL_NOVTABLE KsuidLite {
  virtual ~KsuidLite() = default;

  /**
   * Construct KSUID from raw data.
   *
   * @param data KSUID data bytes.
   * @param data_size must be equal to 20.
   */
  virtual void assign(const uint8_t* data, size_t data_size) = 0;
  /**
   * Construct KSUID from timestamp and random.
   *
   * @param ts timestamp in milliseconds;
   * @param payload payload data;
   * @param payload_size payload data size;
   */
  virtual void assign(int64_t ts, const uint8_t* payload, size_t payload_size) = 0;
  /**
   * Construct KSUID from auto-generated timestamp and payload.
   *
   * @param payload payload data;
   * @param payload_size payload data size;
   */
  virtual void assign_from_payload(const uint8_t* payload, size_t payload_size) = 0;

  /**
   * Timestamp in milliseconds for the KSUID.
   */
  virtual int64_t timestamp_millis() const = 0;
  /**
   * Random bytes for the KSUID.
   */
  virtual MemoryView payload() const = 0;
  /**
   * Raw binary representation of the KSUID.
   */
  virtual MemoryView raw() const = 0;

  virtual bool empty() const = 0;
  virtual bool operator<(const KsuidLite& other) const = 0;
  virtual bool operator<=(const KsuidLite& other) const = 0;
  virtual bool operator==(const KsuidLite& other) const = 0;
  virtual bool operator!=(const KsuidLite& other) const = 0;
};

template <size_t TIMESTAMP_SIZE> class KsuidImpl : public KsuidLite {
public:
  KsuidImpl() = default;

  void assign(const uint8_t* data, size_t data_size) override {
    if (data_size != _BYTE_SIZE) {
      throw std::invalid_argument("data_size must be 20");
    }

    std::copy(data, data + _BYTE_SIZE, _data.begin());
  }

  void assign(int64_t ts, const uint8_t* payload, size_t payload_size) override {
    static_assert(TIMESTAMP_SIZE >= 4 && TIMESTAMP_SIZE <= 6, "invalid timestamp size");

    if (payload_size + TIMESTAMP_SIZE > 20) {
      throw std::invalid_argument("payload size must be <= 20");
    }

    std::lldiv_t dv = std::lldiv(ts, 1000);
    dv.quot -= KSUID_EPOCH;

    // Common code for converting seconds into bytes
    _data[0] = (dv.quot >> 24) & 0xff;
    _data[1] = (dv.quot >> 16) & 0xff;
    _data[2] = (dv.quot >> 8) & 0xff;
    _data[3] = (dv.quot >> 0) & 0xff;

    switch (TIMESTAMP_SIZE) {
    case 4: // 32-bits, the standard
      break;
    case 5:                            // 40-bits, svix's
      _data[4] = (dv.rem >> 2) & 0xff; // round, 4ms precision
      break;
    case 6: // 48-bits
      _data[4] = (dv.rem >> 8) & 0xff;
      _data[5] = (dv.rem >> 0) & 0xff;
      break;
    }

    std::copy(payload, payload + payload_size, _data.begin() + TIMESTAMP_SIZE);
  }

  void assign_from_payload(const uint8_t* payload, size_t payload_size) override {
    // Timestamp
    int64_t timestamp_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                               std::chrono::system_clock::now().time_since_epoch())
                               .count();
    return assign(timestamp_ms, payload, payload_size);
  }

  int64_t timestamp_millis() const noexcept override {
    static_assert(TIMESTAMP_SIZE >= 4 && TIMESTAMP_SIZE <= 6, "invalid timestamp size");

    int64_t ts_s = (static_cast<int64_t>(_data[0]) << 24) | (static_cast<int64_t>(_data[1]) << 16) |
                   (static_cast<int64_t>(_data[2]) << 8) | (static_cast<int64_t>(_data[3]) << 0);
    int64_t ts_ms = 0;

    switch (TIMESTAMP_SIZE) {
    case 4: // 32-bits, the standard
      break;
    case 5: // 40-bits, svix's
      ts_ms = (static_cast<int64_t>(_data[4]) << 2) % 1000;
      break;
    case 6: // 48-bits
      ts_ms = (static_cast<int64_t>(_data[4]) << 8) | (static_cast<int64_t>(_data[5]) << 0);
      break;
    }

    return (ts_s + KSUID_EPOCH) * 1000 + ts_ms;
  }

  MemoryView payload() const noexcept override {
    return MemoryView{
        _data.data() + TIMESTAMP_SIZE,
        _data.size() - TIMESTAMP_SIZE,
    };
  }

  MemoryView raw() const noexcept override {
    return MemoryView{
        _data.data(),
        _data.size(),
    };
  }

  bool empty() const noexcept override {
    static constexpr uint8_t zero[_BYTE_SIZE] = {0};
    return std::memcmp(_data.data(), zero, _BYTE_SIZE) == 0;
  }

  bool operator<(const KsuidLite& other) const noexcept override {
    return std::memcmp(_data.data(), other.raw().data, _BYTE_SIZE) < 0;
  }

  bool operator<=(const KsuidLite& other) const noexcept override {
    return std::memcmp(_data.data(), other.raw().data, _BYTE_SIZE) <= 0;
  }

  bool operator==(const KsuidLite& other) const noexcept override {
    return std::memcmp(_data.data(), other.raw().data, _BYTE_SIZE) == 0;
  }

  bool operator!=(const KsuidLite& other) const noexcept override {
    return std::memcmp(_data.data(), other.raw().data, _BYTE_SIZE) != 0;
  }

private:
  std::array<uint8_t, _BYTE_SIZE> _data;
};

typedef KsuidImpl<4> Ksuid;
typedef KsuidImpl<5> Ksuid40;
typedef KsuidImpl<6> Ksuid48;
