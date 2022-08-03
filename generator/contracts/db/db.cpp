#include <inery/inery.hpp>
#include <string>

using namespace inery;
using namespace std;

class [[inery::contract("db")]] db : public contract {
    public:
        using contract::contract;
        db(name reciever, name code, datastream<const char*> ds ) : contract(reciever, code, ds) {}

	struct [[inery::table("tablcia")]] tablcia {
		uint64_t	id;
		string	name;
		uint64_t primary_key() const {return id; }
	};
	typedef inery::multi_index<"tablcia"_n, tablcia> table_inst0;


	[[inery::action]] void crtablcia (string name) {
		table_inst0  tablcia(get_self(), get_self().value);
		tablcia.emplace(get_self(), [&](auto &row){
			row.id = tablcia.available_primary_key();
			row.name = name;
		});
	}
	[[inery::action]] void uptablcia (uint64_t id, string name) {
		table_inst0  tablcia(get_self(), get_self().value);
		auto itr = tablcia.find(id);
		check(itr != tablcia.end(), "No entity with that id ");
		tablcia.modify(itr, get_self(), [&](auto &row){
			row.name = name;
		});
	}
	[[inery::action]] void dltablcia (uint64_t id) {
		table_inst0  tablcia(get_self(), get_self().value);
		auto itr = tablcia.find(id);
		check(itr != tablcia.end(), "No entity with that id ");
		tablcia.erase(itr);
	}
};