package egovframework.member.service.impl;

import java.util.List;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface MemberMapper {
    String BASE_SELECT = "SELECT member_id, member_nm FROM tb_member";

    // ${} 는 값을 질의문에 그대로 치환한다
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Select("SELECT member_id, member_nm FROM tb_member WHERE member_nm = '${memberNm}'")
    List<MemberVO> selectByName(@Param("memberNm") String memberNm);

    // 이어 붙인 문자열의 뒤쪽에 있는 경우
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Select("SELECT member_id, member_nm FROM tb_member "
            + "ORDER BY ${sortColumn}")
    List<MemberVO> selectAll(@Param("sortColumn") String sortColumn);

    // 상수와 이어 붙인 경우
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Select(BASE_SELECT + " WHERE dept_id = ${deptId}")
    List<MemberVO> selectByDept(@Param("deptId") String deptId);

    // value = 로 적은 경우
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Update(value = "UPDATE tb_member SET member_nm = '${memberNm}' WHERE member_id = #{memberId}")
    int updateName(@Param("memberId") long memberId, @Param("memberNm") String memberNm);

    // 문자열 배열로 적은 경우
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Select({"SELECT member_id, member_nm", "FROM tb_member", "WHERE email = '${email}'"})
    MemberVO selectByEmail(@Param("email") String email);

    // 동적 SQL(<script>) 안
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Select({"<script>",
            "SELECT member_id, member_nm FROM tb_member",
            "<if test='keyword != null'>WHERE member_nm LIKE '%${keyword}%'</if>",
            "</script>"})
    List<MemberVO> search(@Param("keyword") String keyword);

    // 테이블 이름
    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Insert("INSERT INTO ${tableName} (member_id, member_nm) VALUES (#{memberId}, #{memberNm})")
    int insertInto(@Param("tableName") String tableName, @Param("memberId") long memberId, @Param("memberNm") String memberNm);

    // ruleid: mois-1-01-sql-injection-mybatis-annotation
    @Delete(value = {"DELETE FROM tb_member", "WHERE member_id IN (${memberIds})"})
    int deleteAll(@Param("memberIds") String memberIds);
}
